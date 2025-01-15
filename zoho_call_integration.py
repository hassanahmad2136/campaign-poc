import requests

# Zoho CRM OAuth2 Access Token
zoho_access_token = "YOUR_ZOHO_ACCESS_TOKEN"

# RingCentral API Key
ringcentral_api_key = "YOUR_RINGCENTRAL_API_KEY"

# Authorize.net API Credentials
authorize_net_api_login_id = "YOUR_AUTH_NET_API_LOGIN_ID"
authorize_net_transaction_key = "YOUR_AUTH_NET_TRANSACTION_KEY"

# Function to log a call in Zoho CRM
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

# Function to retrieve payment information from Authorize.net
def get_payment_details(transaction_id):
    url = "https://api.authorize.net/xml/v1/request.api"
    headers = {
        "Content-Type": "application/xml",
    }
    xml_payload = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <createTransactionRequest xmlns="AnetApi/xml/v1/schema/AnetApiSchema.xsd">
        <merchantAuthentication>
            <name>{authorize_net_api_login_id}</name>
            <transactionKey>{authorize_net_transaction_key}</transactionKey>
        </merchantAuthentication>
        <transactionRequest>
            <transactionType>json</transactionType>
            <refTransId>{transaction_id}</refTransId>
        </transactionRequest>
    </createTransactionRequest>
    """
    response = requests.post(url, data=xml_payload, headers=headers)
    return response.json()

# Example usage
call_details = {
    "start_time": "2025-01-16T10:00:00Z",
    "duration": "300",
    "description": "Customer inquiry about pricing.",
}
contact_id = "1234567890"  # Replace with actual Zoho contact ID
transaction_id = "TRANSACTION_ID"  # Replace with actual transaction ID from Authorize.net


response_call = log_call_in_zoho(contact_id, call_details)
print("Call Response:", response_call)


response_payment = get_payment_details(transaction_id)
print("Payment Response:", response_payment)
