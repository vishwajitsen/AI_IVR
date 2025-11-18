# fhir_slot.py
import os
import requests

EPIC_FHIR_BASE = os.getenv("EPIC_FHIR_BASE", "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/STU3").rstrip("/")

class FHIRSlot:
    def __init__(self, access_token):
        self.base_url = EPIC_FHIR_BASE
        self.access_token = access_token

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/fhir+json"
        }

    def read_slot(self, slot_id):
        url = f"{self.base_url}/Slot/{slot_id}"
        r = requests.get(url, headers=self._headers(), timeout=30)
        r.raise_for_status()
        return r.json()

    def search_slots(self, practitioner_id=None, start=None, end=None):
        # Epic slot search via Schedule/Slot patterns can vary. This is a naive implementation.
        # You may instead call Appointment/$find for availability (preferred).
        params = {}
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        url = f"{self.base_url}/Slot"
        r = requests.get(url, headers=self._headers(), params=params, timeout=30)
        r.raise_for_status()
        return r.json()
