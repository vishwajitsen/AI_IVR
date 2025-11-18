import os
import requests
from datetime import datetime, timedelta

class EpicAuth:
    def __init__(self):
        self.token_url = os.getenv("EPIC_TOKEN_URL")
        self.client_id = os.getenv("EPIC_CLIENT_ID")
        self.client_secret = os.getenv("EPIC_CLIENT_SECRET")
        self.scope = os.getenv("EPIC_SCOPE").replace('"', '')
        self.username = "FHIRTWO"
        self.password = "EpicFhir11!"
        self.access_token = None
        self.token_expiry = None

    def login(self):
        """
        Provider-facing PASSWORD OAuth for EPIC Sandbox
        """
        payload = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "password": self.password,
            "scope": self.scope
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            response = requests.post(
                self.token_url,
                data=payload,
                headers=headers
            )
            data = response.json()
            print("\n🔵 EPIC LOGIN RESPONSE:", data)

            if "access_token" not in data:
                return None

            self.access_token = data["access_token"]
            expires_in = data.get("expires_in", 3600)
            self.token_expiry = datetime.utcnow() + timedelta(seconds=expires_in)

            return self.access_token

        except Exception as e:
            print("❌ EPIC LOGIN ERROR:", str(e))
            return None

    def get_token(self):
        if not self.access_token or datetime.utcnow() >= self.token_expiry:
            return self.login()
        return self.access_token
