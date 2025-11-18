# epic_oauth.py
import os
import base64
import hashlib
import secrets
import requests
from urllib.parse import urlencode

EPIC_AUTH_BASE = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2"
EPIC_FHIR_BASE = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/STU3"

CLIENT_ID = os.getenv("EPIC_CLIENT_ID")
REDIRECT_URI = os.getenv("EPIC_REDIRECT_URI")
EPIC_SCOPE = os.getenv("EPIC_SCOPE")  # <-- use EXACT scope from .env

if not CLIENT_ID:
    raise Exception("❌ Missing EPIC_CLIENT_ID in .env")
if not REDIRECT_URI:
    raise Exception("❌ Missing EPIC_REDIRECT_URI in .env")
if not EPIC_SCOPE:
    raise Exception("❌ Missing EPIC_SCOPE in .env")

SESSION_STORE = {}


class EpicOAuthClient:
    def __init__(self):
        pass

    # ---------------------------------------------------------
    # Step 1 — Create session & return Epic authorization URL
    # ---------------------------------------------------------
    def create_session(self):
        session_id = secrets.token_urlsafe(16)

        code_verifier = secrets.token_urlsafe(64)
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode()).digest()
        ).rstrip(b"=").decode()

        SESSION_STORE[session_id] = {
            "code_verifier": code_verifier,
            "access_token": None,
        }

        params = {
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "response_type": "code",
            "state": session_id,
            "scope": EPIC_SCOPE,  # 💥 EXACT SCOPE — FIXED
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }

        auth_url = f"{EPIC_AUTH_BASE}/authorize?{urlencode(params)}"
        return session_id, auth_url

    # ---------------------------------------------------------
    # Step 2 — Redeem authorization code for access token
    # ---------------------------------------------------------
    def redeem_code_for_token(self, code, session_id):
        if session_id not in SESSION_STORE:
            return None, "Unknown session_id"

        verifier = SESSION_STORE[session_id]["code_verifier"]

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "code_verifier": verifier,
        }

        resp = requests.post(f"{EPIC_AUTH_BASE}/token", data=data)

        if resp.status_code != 200:
            return None, resp.text

        token_data = resp.json()
        access_token = token_data.get("access_token")

        if access_token:
            SESSION_STORE[session_id]["access_token"] = access_token

            # Save inside .env like your original solution
            with open(".env", "a") as f:
                f.write(f"\nEPIC_ACCESS_TOKEN={access_token}")
                f.write(f"\nEPIC_SESSION_ID={session_id}")

        return token_data, None

    # ---------------------------------------------------------
    # Step 3 — Retrieve stored access token
    # ---------------------------------------------------------
    def get_access_token_for_session(self, session_id):
        session = SESSION_STORE.get(session_id)
        if not session:
            return None
        return session.get("access_token")
