# AI_IVR.py
import os
import json
from dotenv import load_dotenv
load_dotenv()
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()
from flask import Flask, request, redirect, jsonify
from epic_oauth import EpicOAuthClient
from fhir_appointment import FHIRAppointmentClient

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")

oauth = EpicOAuthClient()


# -----------------------------------------------------------
# Helper — overwrite .env with latest EPIC session+token
# -----------------------------------------------------------
def save_epic_credentials(session_id, access_token, expires_in):
    env_path = ".env"

    # Convert expiry seconds → absolute UNIX timestamp
    import time
    expires_at = int(time.time()) + int(expires_in)

    # Read existing .env
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()

    # Remove old entries
    filtered = []
    for line in lines:
        if not (
            line.startswith("EPIC_SESSION_ID=")
            or line.startswith("EPIC_ACCESS_TOKEN=")
            or line.startswith("EPIC_ACCESS_EXPIRES=")
        ):
            filtered.append(line)

    # Add updated values
    filtered.append(f"EPIC_SESSION_ID={session_id}\n")
    filtered.append(f"EPIC_ACCESS_TOKEN={access_token}\n")
    filtered.append(f"EPIC_ACCESS_EXPIRES={expires_at}\n")

    # Save back
    with open(env_path, "w") as f:
        f.writelines(filtered)

    print("✅ Updated .env with latest Epic OAuth credentials")


# -----------------------------------------------------------
# 1) Start Epic Login (PKCE)
# -----------------------------------------------------------
@app.route("/epic/start", methods=["GET"])
def start_epic_auth():
    session_id, auth_url = oauth.create_session()
    print(f"🔵 Redirecting to Epic OAuth: {auth_url}")
    return redirect(auth_url)


# -----------------------------------------------------------
# 2) OAuth Callback — get Epic token
# -----------------------------------------------------------
@app.route("/epic_callback", methods=["GET"])
def epic_callback():
    code = request.args.get("code")
    state = request.args.get("state")

    if not code or not state:
        return jsonify({"error": "missing_code_or_state"}), 400

    print("🔵 Epic returned code:", code)

    token_data, err = oauth.redeem_code_for_token(code, state)
    if err:
        print("❌ Token exchange failed:", err)
        return jsonify({"error": "token_exchange_failed", "details": err}), 500

    # Save the credentials into .env
    save_epic_credentials(
        session_id=state,
        access_token=token_data["access_token"],
        expires_in=token_data.get("expires_in", 3600)
    )

    return jsonify({
        "success": True,
        "session_id": state,
        "access_token_expires_in": token_data.get("expires_in", 3600),
        "token_saved_to_env": True
    })


# -----------------------------------------------------------
# 3) Get patient appointments using /appointment/find
# -----------------------------------------------------------
@app.route("/appointment/find", methods=["POST"])
def appointment_find():
    body = request.get_json(force=True)
    session_id = body.get("session_id")
    patient_id = body.get("patient_id")

    if not session_id or not patient_id:
        return jsonify({"error": "session_id and patient_id required"}), 400

    access_token = oauth.get_access_token_for_session(session_id)
    if not access_token:
        return jsonify({"error": "Epic not authenticated"}), 403

    fhir = FHIRAppointmentClient(access_token)
    results = fhir.find_slots_for_patient(patient_id)

    return jsonify({"session_id": session_id, "results": results})


# -----------------------------------------------------------
# 4) Book an appointment
# -----------------------------------------------------------
@app.route("/appointment/book", methods=["POST"])
def appointment_book():
    body = request.get_json(force=True)
    session_id = body.get("session_id")
    patient_id = body.get("patient_id")
    appointment_id = body.get("appointment_id")

    if not session_id or not patient_id or not appointment_id:
        return jsonify({"error": "session_id, patient_id, appointment_id required"}), 400

    access_token = oauth.get_access_token_for_session(session_id)
    if not access_token:
        return jsonify({"error": "Epic not authenticated"}), 403

    fhir = FHIRAppointmentClient(access_token)
    booked = fhir.book_appointment(patient_id, appointment_id)

    return jsonify({"session_id": session_id, "appointment": booked})


# -----------------------------------------------------------
# Health check
# -----------------------------------------------------------
@app.route("/", methods=["GET"])
def health():
    return "AI IVR - Epic PKCE Server Running"


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"🚀 Starting AI_IVR Flask app on port {port}")
    app.run(host="0.0.0.0", port=port)
