import os
import sys
import requests
from importlib.machinery import SourceFileLoader
from decimal import Decimal

from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *


constants = SourceFileLoader('modulename', 'constants.py').load_module()

# Zoho CRM OAuth2 Access Token
zoho_access_token = "YOUR_ZOHO_ACCESS_TOKEN"

# RingCentral API Key
ringcentral_api_key = "YOUR_RINGCENTRAL_API_KEY"

# Function to retrieve payment details from Authorize.net
def get_transaction_details(transId):
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = constants.apiLoginId
    merchantAuth.transactionKey = constants.transactionKey

    transactionDetailsRequest = apicontractsv1.getTransactionDetailsRequest()
    transactionDetailsRequest.merchantAuthentication = merchantAuth
    transactionDetailsRequest.transId = transId

    transactionDetailsController = getTransactionDetailsController(transactionDetailsRequest)
    transactionDetailsController.execute()
    
    transactionDetailsResponse = transactionDetailsController.getresponse()

    if transactionDetailsResponse is not None:
        if transactionDetailsResponse.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            print('Successfully got transaction details!')
            # Extract details
            transaction_info = {
                'transaction_id': transactionDetailsResponse.transaction.transId,
                'transaction_type': transactionDetailsResponse.transaction.transactionType,
                'transaction_status': transactionDetailsResponse.transaction.transactionStatus,
                'auth_amount': Decimal(transactionDetailsResponse.transaction.authAmount),
                'settle_amount': Decimal(transactionDetailsResponse.transaction.settleAmount),
            }
            if hasattr(transactionDetailsResponse.transaction, 'tax'):
                transaction_info['tax'] = Decimal(transactionDetailsResponse.transaction.tax.amount)
            if hasattr(transactionDetailsResponse.transaction, 'profile'):
                transaction_info['customer_profile_id'] = transactionDetailsResponse.transaction.profile.customerProfileId
            return transaction_info
        else:
            if transactionDetailsResponse.messages is not None:
                print('Failed to get transaction details.\nCode:%s \nText:%s' % (
                    transactionDetailsResponse.messages.message[0]['code'].text,
                    transactionDetailsResponse.messages.message[0]['text'].text
                ))
    return None

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

# Example usage
call_details = {
    "start_time": "2025-01-16T10:00:00Z",
    "duration": "300",
    "description": "Customer inquiry about pricing.",
}

contact_id = "1234567890"  # Replace with actual Zoho contact ID
transaction_id = "TRANSACTION_ID"  # Replace with actual transaction ID from Authorize.net


transaction_info = get_transaction_details(transaction_id)
if transaction_info:
    print("Transaction Details:", transaction_info)
    response_call = log_call_in_zoho(contact_id, call_details)
    print("Call Response:", response_call)
else:
    print("Failed to retrieve transaction details.")
