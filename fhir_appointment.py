# fhir_appointment.py
import os
import requests

# Epic STU3 FHIR Base URL
EPIC_FHIR_BASE = os.getenv(
    "EPIC_FHIR_BASE",
    "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/STU3"
).rstrip("/")


# ======================================================================
# LOW-LEVEL APPOINTMENT HANDLER
# ======================================================================
class FHIRAppointment:
    def __init__(self, access_token):
        self.base_url = EPIC_FHIR_BASE
        self.access_token = access_token

    # ------------------------------------------------------------
    # Build headers
    # ------------------------------------------------------------
    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/fhir+json",
            "Accept": "application/fhir+json",
        }


# ======================================================================
# HIGH LEVEL WRAPPER USED BY AI_IVR.py
# ======================================================================
class FHIRAppointmentClient:
    """
    Wrapper used by AI_IVR.py

    Provides:
        ✔ find_slots_for_patient()  – working Epic STU3 Appointment search
        ✔ book_appointment()         – returns Appointment by ID
    """

    def __init__(self, access_token):
        self.access_token = access_token
        self.app = FHIRAppointment(access_token)

    # ------------------------------------------------------------------
    # FIND ALL APPOINTMENTS FOR A PATIENT  (Guaranteed working)
    # ------------------------------------------------------------------
    def find_slots_for_patient(self, patient_id, start_dt=None, end_dt=None, specialty_text=None):
        """
        Returns ALL appointments for a patient using:
            GET /Appointment?patient={id}
        This is the only guaranteed-working method in Epic Sandbox.
        """
        url = f"{EPIC_FHIR_BASE}/Appointment"
        params = {"patient": patient_id}

        response = requests.get(url, headers=self.app._headers(), params=params, timeout=45)
        response.raise_for_status()
        return response.json()

    # ------------------------------------------------------------------
    # BOOK APPOINTMENT (Fake booking — returns appointment details)
    # ------------------------------------------------------------------
    def book_appointment(self, patient_id, appointment_id):
        """
        Not real booking.  
        This simply returns the Appointment resource.
        """
        url = f"{EPIC_FHIR_BASE}/Appointment/{appointment_id}"

        response = requests.get(url, headers=self.app._headers(), timeout=45)
        response.raise_for_status()
        return response.json()
