# Daraja API Troubleshooting Guide

## Current Issue
Getting "Invalid Access Token" (404.001.03) when calling STK Push, even though token generation succeeds.

## Root Cause
Your consumer key/secret are likely from a Daraja app that doesn't have "Lipa Na M-Pesa Online" enabled, or you're using mismatched credentials.

## Solution Steps

### 1. Verify Your Daraja App Configuration

Go to: https://developer.safaricom.co.ke/MyApps

Check your app and ensure:
- ✓ "Lipa Na M-Pesa Online" product is added to your app
- ✓ The consumer key matches: ARYM9ADDeo...
- ✓ The app is in "Sandbox" environment

### 2. Create a New App (If Needed)

If your current app doesn't have STK Push:

1. Go to https://developer.safaricom.co.ke/MyApps
2. Click "Create New App"
3. Add these products:
   - Lipa Na M-Pesa Online (for STK Push)
   - M-Pesa Sandbox (for testing)
4. Copy the NEW consumer key and secret
5. Update your settings.py with the new credentials

### 3. Use the Correct Test Credentials

For Safaricom Sandbox, you MUST use:
- Shortcode: 174379
- Passkey: bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919
- Test Phone: 254708374149 (official test number)

Your phone (254746836004) might not work in sandbox - use the official test number.

### 4. Alternative: Try the Official Daraja Test Credentials

If you're just testing, you can use the public test credentials:

Consumer Key: (Get from a fresh sandbox app)
Consumer Secret: (Get from a fresh sandbox app)

### 5. Check API Permissions

Sometimes the sandbox API has issues. Try:
- Logging out and back into the Daraja portal
- Regenerating your consumer key/secret
- Waiting 5-10 minutes after creating/updating an app

## Common Mistakes

❌ Using consumer key from one app with shortcode from another
❌ Not having "Lipa Na M-Pesa Online" enabled on your app
❌ Using production credentials in sandbox environment
❌ Using a phone number that's not registered for sandbox testing

## Next Steps

1. Log into https://developer.safaricom.co.ke
2. Check your app's products
3. If STK Push is not enabled, create a new app with it enabled
4. Update your credentials in settings.py
5. Use the official test phone number: 254708374149
