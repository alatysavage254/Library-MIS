#!/usr/bin/env python
"""
Test script to verify M-Pesa API token and STK Push
Run this to debug M-Pesa integration issues
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

def test_access_token():
    """Test getting access token"""
    print("\n" + "="*60)
    print("TESTING ACCESS TOKEN")
    print("="*60)
    
    consumer_key = settings.MPESA_CONSUMER_KEY.strip()
    consumer_secret = settings.MPESA_CONSUMER_SECRET.strip()
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    print(f"\nConsumer Key: {consumer_key[:10]}...{consumer_key[-10:]}")
    print(f"Consumer Secret: {consumer_secret[:10]}...{consumer_secret[-10:]}")
    print(f"API URL: {api_url}")
    
    try:
        response = requests.get(
            api_url,
            auth=HTTPBasicAuth(consumer_key, consumer_secret),
            verify=True
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token', '').strip()
            print(f"\n✓ Token obtained successfully!")
            print(f"Token: {token[:15]}...{token[-15:]}")
            print(f"Token Length: {len(token)}")
            print(f"Expires In: {data.get('expires_in')} seconds")
            return token
        else:
            print(f"\n✗ Failed to get token")
            return None
            
    except Exception as e:
        print(f"\n✗ Exception: {str(e)}")
        return None

def test_stk_push(access_token):
    """Test STK Push with the access token"""
    print("\n" + "="*60)
    print("TESTING STK PUSH")
    print("="*60)
    
    # Test credentials
    phone_number = "254746836004"  # Your test number
    amount = 1  # Minimum amount for testing
    account_reference = "TEST001"
    transaction_desc = "Test Payment"
    
    # Generate timestamp and password
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    shortcode = str(settings.MPESA_EXPRESS_SHORTCODE).strip()
    passkey = str(settings.MPESA_PASSKEY).strip()
    
    data_to_encode = shortcode + passkey + timestamp
    password = base64.b64encode(data_to_encode.encode()).decode('utf-8')
    
    print(f"\nShortcode: {shortcode}")
    print(f"Timestamp: {timestamp}")
    print(f"Password: {password[:20]}...")
    
    # Prepare payload
    payload = {
        'BusinessShortCode': shortcode,
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': amount,
        'PartyA': phone_number,
        'PartyB': shortcode,
        'PhoneNumber': phone_number,
        'CallBackURL': f'{settings.NGROK_URL}/handle/payment/transactions',
        'AccountReference': account_reference,
        'TransactionDesc': transaction_desc
    }
    
    print(f"\nPayload:")
    print(json.dumps(payload, indent=2))
    
    # Prepare headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    print(f"\nHeaders:")
    print(f"Authorization: Bearer {access_token[:15]}...{access_token[-15:]}")
    print(f"Content-Type: application/json")
    
    # Make request
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    
    try:
        response = requests.post(
            api_url,
            json=payload,
            headers=headers,
            verify=True,
            timeout=30
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ResponseCode') == '0':
                print(f"\n✓ STK Push sent successfully!")
                print(f"Merchant Request ID: {data.get('MerchantRequestID')}")
                print(f"Checkout Request ID: {data.get('CheckoutRequestID')}")
                return True
            else:
                print(f"\n✗ STK Push failed: {data.get('ResponseDescription')}")
                return False
        else:
            print(f"\n✗ Request failed with status {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error Code: {error_data.get('errorCode')}")
                print(f"Error Message: {error_data.get('errorMessage')}")
            except:
                pass
            return False
            
    except Exception as e:
        print(f"\n✗ Exception: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("M-PESA API TEST SCRIPT")
    print("="*60)
    
    # Test 1: Get access token
    token = test_access_token()
    
    if not token:
        print("\n✗ Cannot proceed without access token")
        return
    
    # Test 2: Try STK Push
    input("\nPress Enter to test STK Push (or Ctrl+C to cancel)...")
    test_stk_push(token)
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)

if __name__ == '__main__':
    main()
