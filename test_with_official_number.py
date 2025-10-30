#!/usr/bin/env python
"""
Test M-Pesa with the official Safaricom test number
This uses the exact format that Safaricom expects
"""
import os
import sys
import django
import json
import base64
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()

from django.conf import settings

def get_token():
    """Get access token"""
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    response = requests.get(
        url,
        auth=HTTPBasicAuth(
            settings.MPESA_CONSUMER_KEY,
            settings.MPESA_CONSUMER_SECRET
        )
    )
    
    if response.status_code == 200:
        token = response.json()['access_token']
        print(f"✓ Token: {token}")
        return token
    else:
        print(f"✗ Token failed: {response.text}")
        return None

def stk_push(token):
    """Send STK Push using official test number"""
    
    # Use official Safaricom test credentials
    shortcode = "174379"
    passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    phone = "254708374149"  # Official test number
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()
    
    url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": "https://mydomain.com/callback",
        "AccountReference": "Test123",
        "TransactionDesc": "Test Payment"
    }
    
    print(f"\nSending STK Push to {phone}...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {response.text}")
    
    return response

if __name__ == '__main__':
    print("="*60)
    print("M-PESA STK PUSH TEST - Official Test Number")
    print("="*60)
    
    token = get_token()
    if token:
        stk_push(token)
    
    print("\n" + "="*60)
    print("\nIMPORTANT:")
    print("If this still fails with 'Invalid Access Token', your")
    print("Daraja app does NOT have STK Push enabled.")
    print("\nGo to: https://developer.safaricom.co.ke/MyApps")
    print("And ensure 'Lipa Na M-Pesa Online' is added to your app.")
    print("="*60)
