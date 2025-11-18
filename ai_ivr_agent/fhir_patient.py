# fhir_patient.py
import os
import requests

EPIC_FHIR_BASE = os.getenv("EPIC_FHIR_BASE", "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/STU3").rstrip("/")

class FHIRPatient:
    def __init__(self, access_token):
        self.base_url = EPIC_FHIR_BASE
        self.access_token = access_token

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/fhir+json"
        }

    def read_patient(self, patient_id):
        url = f"{self.base_url}/Patient/{patient_id}"
        r = requests.get(url, headers=self._headers(), timeout=30)
        r.raise_for_status()
        return r.json()
