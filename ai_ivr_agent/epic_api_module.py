import os
import requests
import json
from dotenv import load_dotenv
from epic_oauth import EpicOAuth

load_dotenv()

class EpicFHIR:
    def __init__(self):
        self.fhir_base = os.getenv("EPIC_FHIR_BASE")
        self.group_id = os.getenv("EPIC_GROUP_ID")
        self.token = EpicOAuth().get_token()
        self.headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/fhir+json"}

    def get_metadata(self):
        url = f"{self.fhir_base}/metadata"
        return requests.get(url, headers=self.headers)

    def get_patient(self, patient_id):
        url = f"{self.fhir_base}/Patient/{patient_id}"
        return requests.get(url, headers=self.headers)

    def find_appointments(self):
        url = f"{self.fhir_base}/Appointment/$find"
        payload = {
            "resourceType": "Parameters",
            "parameter": [
                {"name": "startTime", "valueDateTime": "2024-05-01T13:00:00Z"},
                {"name": "endTime", "valueDateTime": "2028-05-05T22:00:00Z"},
                {"name": "serviceType", "valueCodeableConcept": {"coding": [{"code": "95014", "display": "Office Visit"}]}},
            ],
        }
        return requests.post(url, headers=self.headers, json=payload)

    def bulk_export_kickoff(self):
        url = f"{self.fhir_base}/Group/{self.group_id}/$export"
        return requests.get(url, headers={**self.headers, "Prefer": "respond-async"})

    def bulk_export_status(self, status_url):
        return requests.get(status_url, headers=self.headers)

    def bulk_export_delete(self, delete_url):
        return requests.delete(delete_url, headers=self.headers)
