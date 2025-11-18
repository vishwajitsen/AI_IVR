import requests
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()
ACCESS_TOKEN = """eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ1cm46b2lkOjEuMi44NDAuMTE0MzUwLjEuMTMuMC4xLjcuMy42ODg4ODQuMTAwIiwiY2xpZW50X2lkIjoiZWI1ZWEwYTItNDYwMC00N2Y0LWExODktZDcwNTE4MDg4OTAzIiwiZXBpYy5lY2kiOiJ1cm46ZXBpYzpPcGVuLkVwaWMtY3VycmVudCIsImVwaWMubWV0YWRhdGEiOiJaTEpQS2R2UXJ6cEN2T1pfa2Fnbmp2cWJ3VmlyQVBSUERfbHJGbmh0UHRzY21JZGtmQXZqa3VaU0V4WmgxTWtRUGctSnRheS1DdG8yWVBJbDNRUGNmSFVfVkxYRGRwNzdfUjlhejQ3aWFlQXZBVlMtenpURE5SRlB3ZzNWMUlLNCIsImVwaWMudG9rZW50eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYzNDUyNTY2LCJpYXQiOjE3NjM0NDg5NjYsImlzcyI6InVybjpvaWQ6MS4yLjg0MC4xMTQzNTAuMS4xMy4wLjEuNy4zLjY4ODg4NC4xMDAiLCJqdGkiOiIxZjg2MmI2Yi03MDRkLTQwMDYtYTk3ZC0zZjJiNTZhZjNhYzMiLCJuYmYiOjE3NjM0NDg5NjYsInN1YiI6ImUzTUJYQ09tY29MS2w3YXlMRDUxQVdBMyJ9.IjfWyKURAnDnvtraGiCR7c1pXiddnx5ONk88PtrcSIdSzayTbuUGZfXu9trRBhaNc9-KQezF1OlMfbfMnMbnCKZhORqV_zEqngsTJGHFjkTi5s6Fe4lvr7S7NGJ9OcB4XzaVt6fPDhoOY5a-xptC4M4dauJdNFzKqoHCxmnXWoW_DZ4_OaZFR8_uvi_qgjvZrVb9dFQ4xyVRMHmLe9CP7o3CXq5LWQ1kb-JwT_Q0GQVgpiTLhSv-fBGBh_spuQDiotEiLcgRSoEm0JEkoLVNxskU8xIFKcpfT1p2_99fHeObbthEXKleFLapHu-bzz6qRjcg2_ZU8VZ1b-utHdUSuQ""".replace("\n", "").strip()

APPOINTMENT_ID = "eGFFFp0KKaZdjgF36sTfrjXaLjBH89aU3nWCXNCrJ4x03"  # from your list

url = f"https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/STU3/Appointment/{APPOINTMENT_ID}"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/fhir+json"
}

print("➡ Requesting appointment:", APPOINTMENT_ID)
response = requests.get(url, headers=headers)

print("➡ Status:", response.status_code)
print("➡ Body:\n", response.text)
