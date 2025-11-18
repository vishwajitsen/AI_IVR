"""
test_epic_integration.py
Light test script to validate metadata, patient read, Appointment/$find and Appointment/$book flows.
It uses EPIC_ACCESS_TOKEN from .env or you can create a session using the Flask app to obtain one.
"""

import os
import requests
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()

EPIC_FHIR_BASE = os.getenv("EPIC_FHIR_BASE")
ACCESS_TOKEN = os.getenv("EPIC_ACCESS_TOKEN", "").strip().strip("'\"")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/fhir+json",
    "Content-Type": "application/fhir+json"
}

print("=== STEP 1: metadata ===")
meta_url = f"{EPIC_FHIR_BASE}/metadata"
r = requests.get(meta_url, headers={"Accept":"application/fhir+json"})
print(meta_url, "->", r.status_code)
if r.status_code == 200:
    print("Metadata OK")
else:
    print("Metadata response snippet:", r.text[:400])

print("\n=== STEP 2: read patient ===")
test_patient = os.getenv("TEST_PATIENT_ID", "cf-Patient-1")
patient_url = f"{EPIC_FHIR_BASE}/Patient/{test_patient}"
r = requests.get(patient_url, headers=headers)
print(patient_url, "->", r.status_code)
if r.status_code == 200:
    print("Patient read OK, name:", r.json().get("name", [{}])[0])
else:
    print("Patient read failed snippet:", r.text[:400])

print("\n=== STEP 3: Appointment $find ===")
find_url = f"{EPIC_FHIR_BASE}/Appointment/$find"
# sample window: now -> +7 days
now = datetime.utcnow()
start = now.strftime("%Y-%m-%dT%H:%M:%SZ")
end = (now + (timezone.utc.utcoffset(now) if False else (now - now))).strftime("%Y-%m-%dT%H:%M:%SZ")
# Use a simple window; adjust as appropriate
body = {
    "resourceType": "Parameters",
    "parameter": [
        {"name":"patient", "resource": {"resourceType":"Patient", "id": test_patient}},
        {"name":"startTime","valueDateTime": start},
        {"name":"endTime","valueDateTime": (now + timedelta(days=14)).strftime("%Y-%m-%dT%H:%M:%SZ")}
    ]
}

r = requests.post(find_url, headers=headers, json=body)
print("POST", find_url, "->", r.status_code)
if r.status_code == 200:
    j = r.json()
    print("find returned total:", j.get("total"))
    # print first entry if any
    entries = j.get("entry", [])
    if entries:
        print("First appointment id:", entries[0].get("resource", {}).get("id"))
else:
    print("find failed snippet:", r.text[:400])

print("\n=== Done ===")




curl -X POST http://127.0.0.1:5000/appointment/find \
  -H "Content-Type: application/json" \
  -d '{"session_id":"-YIK9a_h4q95XBqn","patient_id":"erXuFYUfucBZaryVksYEcMg3"}'




curl -X POST http://127.0.0.1:5000/appointment/book \
  -H "Content-Type: application/json" \
  -d '{"session_id":"<session_id>","patient_id":"<patient_id>","appointment_id":"<appointment_id>"}'
