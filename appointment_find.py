# appointment_find.py

#work in this ConnectionAbortedError
import os
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

EPIC_BASE = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/STU3"

ACCESS_TOKEN = os.getenv("EPIC_ACCESS_TOKEN")
PATIENT_ID = "erXuFYUfucBZaryVksYEcMg3"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/fhir+json",
}

url = f"{EPIC_BASE}/Appointment"
params = {"patient": PATIENT_ID}

print("➡ Searching appointments for patient:", PATIENT_ID)
resp = requests.get(url, headers=headers, params=params)

print("➡ Status:", resp.status_code)
print("➡ Response Body:\n", resp.text)
