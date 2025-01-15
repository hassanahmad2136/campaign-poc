import requests

# Zoho CRM OAuth2 Access Token
zoho_access_token = "YOUR_ZOHO_ACCESS_TOKEN"

# RingCentral API Key
ringcentral_api_key = "YOUR_RINGCENTRAL_API_KEY"

def log_call_in_zoho(contact_id, call_details):
    url = f"https://www.zohoapis.com/crm/v2/Calls"
    headers = {
        "Authorization": f"Zoho-oauthtoken {zoho_access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "data": [
            {
                "Call_Type": "Inbound",
                "Call_Start_Time": call_details["start_time"],
                "Call_Duration": call_details["duration"],
                "Contact_Name": contact_id,
                "Description": call_details["description"],
            }
        ]
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

call_details = {
    "start_time": "2025-01-16T10:00:00Z",
    "duration": "300",
    "description": "Customer inquiry about pricing.",
}
contact_id = "1234567890" # Replace with actual contact id in zoho
response = log_call_in_zoho(contact_id, call_details)
print(response)
