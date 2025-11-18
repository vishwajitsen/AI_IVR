# fhir_practitioner.py
import os
import requests

EPIC_FHIR_BASE = os.getenv("EPIC_FHIR_BASE", "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/STU3").rstrip("/")

class FHIRPractitioner:
    def __init__(self, access_token):
        self.base_url = EPIC_FHIR_BASE
        self.access_token = access_token

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/fhir+json"
        }

    def read_practitioner(self, practitioner_id):
        url = f"{self.base_url}/Practitioner/{practitioner_id}"
        r = requests.get(url, headers=self._headers(), timeout=30)
        r.raise_for_status()
        return r.json()

    def search_practitioner_by_user(self, username):
        # Simple convenience search by name/display - adapt as needed
        url = f"{self.base_url}/Practitioner?name={username}"
        r = requests.get(url, headers=self._headers(), timeout=30)
        r.raise_for_status()
        return r.json()
