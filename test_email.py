

# ----------------------------
# 1. Your EPIC ACCESS TOKEN
# ----------------------------



import requests

ACCESS_TOKEN = """
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ1cm46b2lkOjEuMi44NDAuMTE0MzUwLjEuMTMuMC4xLjcuMy42ODg4ODQuMTAwIiwiY2xpZW50X2lkIjoiZWI1ZWEwYTItNDYwMC00N2Y0LWExODktZDcwNTE4MDg4OTAzIiwiZXBpYy5lY2kiOiJ1cm46ZXBpYzpPcGVuLkVwaWMtY3VycmVudCIsImVwaWMubWV0YWRhdGEiOiJEYXM0eHJHOXo3R3pQbGVyeTB2YV9IbGlNbWVUZXJPMlhJdGs1TDBWdVlUa3h5Q2FsLVVnSUplMUZZZUpTcEtOMHU4cmNSbF9xN3JEbkY3NG8zM25ObmZqV0NMOGZIVXJsMjI4RERyQzZvNmFmVHBOWDhBQVhTb2RzNHFfMjhROCIsImVwaWMudG9rZW50eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYzNDQ2MjcxLCJpYXQiOjE3NjM0NDI2NzEsImlzcyI6InVybjpvaWQ6MS4yLjg0MC4xMTQzNTAuMS4xMy4wLjEuNy4zLjY4ODg4NC4xMDAiLCJqdGkiOiI4YWNlODUxMy0xYTI1LTQ4ZjctODJlMi02NjhkOTM2YTkzNzkiLCJuYmYiOjE3NjM0NDI2NzEsInN1YiI6ImUzTUJYQ09tY29MS2w3YXlMRDUxQVdBMyJ9.WeDn9jUqxE7EJeJKXpDc5XHbWAifocv1c0-8KnSHPczaUjysDXfGZoRq4KD3AmhZs2-uyTSKvxAcIfSJNFmI4gGE390UaWrLlirGNdlB2qug-QoD4Kh0WnYzh7vhq2vgQw2ZAryyKKiF6x5enN_NsyCZV7o3uo_nOutc2zGgVBRBAv13IbkPGsWUa-IhRAqa8cInHCRXUaZOxT4q94W_tNXK--l7ocDiti6a17oHlgcx1HOp1o3yaASZzR3_toN0XQ7O9i4O1yrurCLtT3ZsJNDhkV7d9ZiIfQRJtYWF5z6Oqapii-dcv8uUclLAAe8bYJOQQxkadvVkwD2zCN71Jw
""".replace("\n", "").strip()
patient_id = "erXuFYUfucBZaryVksYEcMg3"

url = f"https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/STU3/Patient/{patient_id}"
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Accept": "application/fhir+json"}

print(requests.get(url, headers=headers).text)
