# fhir_appointment_advanced.py
import os
import requests
from datetime import datetime

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Epic STU3 FHIR Base URL
EPIC_FHIR_BASE = os.getenv(
    "EPIC_FHIR_BASE",
    "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/STU3"
).rstrip("/")


# ======================================================================
# LOW LEVEL APPOINTMENT FHIR WRAPPER
# ======================================================================
class FHIRAppointmentAdvanced:
    def __init__(self, access_token):
        self.base_url = EPIC_FHIR_BASE
        self.access_token = access_token

    # ------------------------------------------------------------
    # Authentication Headers
    # ------------------------------------------------------------
    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/fhir+json",
            "Accept": "application/fhir+json",
        }

    # ------------------------------------------------------------
    # Helper: CodeableConcept
    # ------------------------------------------------------------
    def cc(self, system, code, display=None):
        return {
            "coding": [
                {
                    "system": system,
                    "code": code,
                    "display": display or code
                }
            ]
        }

    # ============================================================
    # 1. REAL OPEN TIME SLOTS — Appointment.$find
    # ============================================================
    def find_open_slots(
        self,
        patient_id,
        start_time,
        end_time,
        service_type_code=None,
        service_type_system=None,
        service_type_display=None,
        location_reference=None
    ):
        """
        Uses Epic STU3 Appointment.$find to get AVAILABLE SLOTS.
        """

        url = f"{self.base_url}/Appointment/$find"

        params = {
            "resourceType": "Parameters",
            "parameter": []
        }

        # Required
        params["parameter"].append({
            "name": "patient",
            "valueReference": {"reference": f"Patient/{patient_id}"}
        })

        # Optional
        if start_time:
            params["parameter"].append({"name": "startTime", "valueDateTime": start_time})

        if end_time:
            params["parameter"].append({"name": "endTime", "valueDateTime": end_time})

        if service_type_code and service_type_system:
            params["parameter"].append({
                "name": "serviceType",
                "valueCodeableConcept": self.cc(
                    service_type_system,
                    service_type_code,
                    service_type_display
                )
            })

        if location_reference:
            params["parameter"].append({
                "name": "location-reference",
                "valueReference": {"reference": location_reference}
            })

        response = requests.post(
            url,
            headers=self._headers(),
            json=params,
            timeout=45
        )

        response.raise_for_status()
        return response.json()

    # ============================================================
    # 2. REAL BOOKING — Appointment/$book
    # ============================================================
    def book_appointment(self, slot_id, patient_id):
        """
        Books an appointment using STU3 Appointment/$book
        """
        url = f"{self.base_url}/Appointment/$book"

        booking = {
            "resourceType": "Parameters",
            "parameter": [
                {"name": "slot", "valueReference": {"reference": f"Slot/{slot_id}"}},
                {"name": "patient", "valueReference": {"reference": f"Patient/{patient_id}"}}
            ]
        }

        response = requests.post(
            url,
            headers=self._headers(),
            json=booking,
            timeout=45
        )

        response.raise_for_status()
        return response.json()


# ======================================================================
# HIGH LEVEL CLIENT FOR AI_IVR.py
# ======================================================================
class FHIRAppointmentClient:
    """
    Wrapper used by AI_IVR.py
    """

    def __init__(self, access_token):
        self.app = FHIRAppointmentAdvanced(access_token)

    def find_open_slots(self, patient_id, start, end, st_code=None, st_sys=None, st_disp=None):
        return self.app.find_open_slots(
            patient_id,
            start_time=start,
            end_time=end,
            service_type_code=st_code,
            service_type_system=st_sys,
            service_type_display=st_disp
        )

    def book_slot(self, slot_id, patient_id):
        return self.app.book_appointment(slot_id, patient_id)
