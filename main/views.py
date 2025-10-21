import json
import base64
import requests
from datetime import date, timedelta, datetime
from requests.auth import HTTPBasicAuth

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from main.models import Book, Transaction, Student, Payment

def get_access_token():
    """Get M-Pesa access token"""
    consumer_key = settings.MPESA_CONSUMER_KEY.strip()
    consumer_secret = settings.MPESA_CONSUMER_SECRET.strip()
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    try:
        print(f"\nGetting access token from: {api_URL}")
        print(f"Using consumer key: {consumer_key[:10]}...")
        
        # Use specific headers for token request
        headers = {
            'Content-Type': 'application/json'
        }
        
        r = requests.get(
            api_URL,
            auth=HTTPBasicAuth(consumer_key, consumer_secret),
            headers=headers,
            verify=True
        )
        
        print(f"Access token status code: {r.status_code}")
        print(f"Access token response: {r.text}")
        
        if r.status_code == 200:
            token = r.json().get('access_token', '').strip()
            print(f"Extracted token: {token[:10]}...")
            return token
        else:
            print(f"Error getting access token. Status: {r.status_code}, Response: {r.text}")
            return None
    except Exception as e:
        print(f"Exception getting access token: {str(e)}")
        return None

def generate_password(shortcode, passkey, timestamp):
    """Generate M-Pesa password"""
    shortcode = str(shortcode).strip()
    passkey = str(passkey).strip()
    timestamp = str(timestamp).strip()
    
    print(f"\n=== Generating Password ===")
    print(f"Shortcode: {shortcode}")
    print(f"Timestamp: {timestamp}")
    print(f"Passkey: {passkey[:10]}...")
    
    data_to_encode = shortcode + passkey + timestamp
    print(f"String to encode: {data_to_encode}")
    
    encoded = base64.b64encode(data_to_encode.encode())
    password = encoded.decode('utf-8')
    
    print(f"Generated password: {password}")
    return password

@login_required
# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def books_in_store(request):
    books = Book.objects.all()
    return render(request, 'books_in_store.html', {'books': books})

@login_required
def borrowed_books(request):
    borrowed = Transaction.objects.filter(status='BORROWED')
    return render(request, 'borrowed_books.html', {"borrowed_items": borrowed})

@login_required
def book_fines(request):
    transactions = Transaction.objects.all()
    fines = [t for t in transactions if t.total_fine > 0]
    return render(request, 'book_fines.html', {'fines': fines})

@login_required
def issue_book(request, id):
    book = get_object_or_404(Book, pk=id)
    students = Student.objects.all()
    if request.method == 'POST':
       student_id = request.POST['student_id']
       student = Student.objects.get(pk=student_id)
       expected_return_date = date.today() + timedelta(days=7)
       transaction = Transaction.objects.create(book=book, student=student, expected_return_date=expected_return_date, status='BORROWED')
       transaction.save()
       messages.success(request, f'Book {book.title} was borrowed successfully')
       return redirect('books_in_store')

    return render(request, 'issue.html', {'book': book, 'students': students})

@login_required
def return_book(request, id):
    transaction = get_object_or_404(Transaction, pk=id)
    transaction.return_date = date.today()
    transaction.status = 'RETURNED'
    transaction.save()
    messages.success(request, f'Book {transaction.book.title} was returned successfully')
    if transaction.total_fine > 0:
        messages.warning(request, f'Book {transaction.book.title} has incurred a fine of Ksh.{transaction.total_fine}')
    return redirect('books_in_store')

@login_required
def pay_overdue(request, id):
    try:
        transaction = get_object_or_404(Transaction, pk=id)
        
        # For testing, use the test phone number
        phone = "0746836004"  # Test M-Pesa number
        
        # Format phone number
        phone_number = '254' + phone.lstrip('0')
        
        # Payment details
        amount = int(transaction.total_fine)
        account_reference = transaction.student.adm_no
        transaction_desc = f'Library Fine - {account_reference}'
        
        # Get timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Get access token
        access_token = get_access_token()
        if not access_token:
            messages.error(request, 'Could not get access token from Safaricom')
            return redirect('book_fines')
            
        # Print debug info
        print("\n=== Payment Request Details ===")
        print(f"Phone: {phone_number}")
        print(f"Amount: {amount}")
        print(f"Reference: {account_reference}")
        print(f"Access Token: {access_token[:10]}...")
        
        # Generate password
        password = generate_password(
            settings.MPESA_EXPRESS_SHORTCODE,
            settings.MPESA_PASSKEY,
            timestamp
        )
        
        # Prepare the request
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        
        payload = {
            'BusinessShortCode': settings.MPESA_EXPRESS_SHORTCODE,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': phone_number,
            'PartyB': settings.MPESA_EXPRESS_SHORTCODE,
            'PhoneNumber': phone_number,
            'CallBackURL': f'{settings.NGROK_URL}/handle/payment/transactions',
            'AccountReference': account_reference,
            'TransactionDesc': transaction_desc
        }
        
        print("\n=== STK Push Request ===")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        # Make the request
        api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        
        # Ensure headers are properly formatted
        headers = {
            'Authorization': 'Bearer {}'.format(access_token.strip()),
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        print(f"\n=== Request Details ===")
        print(f"URL: {api_url}")
        print(f"Headers: {headers}")
        print(f"Access Token Used: {access_token}")
        
        try:
            # First verify the API is reachable
            test_response = requests.get('https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', 
                                      auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
            print(f"\nAPI Connectivity Test Response: {test_response.status_code}")
            
            # Now make the actual request
            response = requests.post(
                api_url,
                json=payload,
                headers=headers,
                verify=True,
                timeout=30  # Set a timeout
            )
            
            print(f"\n=== Raw Response ===")
            print(f"Status Code: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            print(f"Body: {response.text}")
            
        except requests.exceptions.RequestException as e:
            print(f"\nRequest Exception: {str(e)}")
            raise
        
        print(f"\n=== STK Push Response ===")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            # Parse the response
            result = response.json()
            if 'ResponseCode' in result and result['ResponseCode'] == '0':
                # Create payment record
                payment = Payment.objects.create(
                    transaction=transaction,
                    merchant_request_id=result.get('MerchantRequestID'),
                    checkout_request_id=result.get('CheckoutRequestID'),
                    amount=amount
                )
                messages.success(request, 'Payment request sent. Please check your phone.')
            else:
                error_msg = result.get('errorMessage', 'Unknown error occurred')
                messages.error(request, f'Payment failed: {error_msg}')
        else:
            messages.error(request, f'Payment request failed. Status: {response.status_code}')
            
    except Exception as e:
        print(f"\n=== Error ===\n{str(e)}")
        messages.error(request, f'Error processing payment: {str(e)}')
        
    return redirect('book_fines')
    
    # Get the callback URL from settings or environment variable
    # During development, update this URL whenever ngrok gives you a new one
    callback_url = f'{settings.NGROK_URL}/handle/payment/transactions' if hasattr(settings, 'NGROK_URL') else 'http://localhost:8000/handle/payment/transactions'
    try:
        # Log all relevant information
        print("\n=== Payment Request Details ===")
        print(f"Phone Number: {phone_number}")
        print(f"Amount: {amount}")
        print(f"Account Reference: {account_reference}")
        print(f"Transaction Description: {transaction_desc}")
        print(f"Callback URL: {callback_url}")
        
        print("\n=== MPESA Settings ===")
        print(f"Environment: {settings.MPESA_ENVIRONMENT}")
        print(f"Express Shortcode: {settings.MPESA_EXPRESS_SHORTCODE}")
        print(f"Consumer Key: {settings.MPESA_CONSUMER_KEY[:10]}...")
        
        # Get a fresh access token
        print("\n=== Getting Access Token ===")
        try:
            access_token_response = cl.access_token()
            print(f"Access Token Response: {access_token_response}")
        except Exception as e:
            print(f"Access Token Error: {str(e)}")
            messages.error(request, f'Failed to get access token: {str(e)}')
            return redirect('book_fines')
        
        # Make the STK push request
        print("\n=== Making STK Push Request ===")
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
        print(f"STK Push Response: {response.__dict__ if hasattr(response, '__dict__') else response}")
        
        # Log the raw response
        print("\n=== M-Pesa API Response ===")
        print(f"Raw Response: {response}")
        print(f"Response Dict: {response.__dict__ if hasattr(response, '__dict__') else 'No dict attribute'}")
        
        if hasattr(response, 'response_code') and response.response_code == "0":
            payment = Payment.objects.create(
                transaction=transaction,
                merchant_request_id=response.merchant_request_id,
                checkout_request_id=response.checkout_request_id,
                amount=amount
            )
            payment.save()
            success_msg = 'Payment request sent successfully. Please check your phone to complete the transaction.'
            print(f"\nSuccess: {success_msg}")
            messages.success(request, success_msg)
        else:
            error_msg = f'Payment request failed. Response: {response}'
            print(f"\nError: {error_msg}")
            messages.error(request, error_msg)
    except Exception as e:
        import traceback
        error_msg = f'Error processing payment: {str(e)}'
        print(f"\n=== Exception Details ===")
        print(error_msg)
        print("Traceback:")
        print(traceback.format_exc())
        messages.error(request, error_msg)
    return redirect('book_fines')

@login_required
@csrf_exempt
def callback(request):
    resp = json.loads(request.body)
    data = resp['Body']['stkCallback']
    if data["ResultCode"] == "0":
        m_id = data["MerchantRequestID"]
        c_id = data["CheckoutRequestID"]
        code =""
        item = data["CallbackMetadata"]["Item"]
        for i in item:
            name = i["Name"]
            if name == "MpesaReceiptNumber":
                code= i["Value"]
        try:
            payment = Payment.objects.get(merchant_request_id=m_id, checkout_request_id=c_id)
            payment.mpesa_receipt = code
            payment.status = "COMPLETED"
            payment.save()
            
            # Update the associated transaction
            transaction = payment.transaction
            transaction.status = "PAID"
            transaction.save()
            
            messages.success(request, f'Payment completed successfully. Receipt: {code}')
        except Payment.DoesNotExist:
            messages.error(request, 'Payment record not found')
    return HttpResponse("OK")

@login_required
def pie_chart(request):
    transactions = Transaction.objects.filter(created_at__year=2024)
    returned = transactions.filter(status='RETURNED').count()
    lost = transactions.filter(status='LOST').count()
    borrowed = transactions.filter(status='BORROWED').count()
    return JsonResponse({
        "title": "Grouped By Status",
        "data": {
            "labels": ["Returned", "Borrowed", "Lost"],
            "datasets": [{
                "data": [returned, lost, borrowed],
                "backgroundColor": ['#4e73df', '#1cc88a', '#36b9cc'],
                "hoverBackgroundColor": ['#2e59d9', '#17a673', '#2c9faf'],
                "hoverBorderColor": "rgba(234, 236, 244, 1)",
            }],
        }
    })

@login_required
def line_chart(request):
    transactions = Transaction.objects.filter(created_at__year=2024)
    grouped  = transactions.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    numbers = []
    months = []
    for i in grouped:
        numbers.append(i['count'])
        months.append(i['month'].strftime("%b"))
    return JsonResponse({
        "title": "Transactions Grouped By Month",
        "data": {
            "labels": months,
            "datasets": [{
                "label": "Count",
                "lineTension": 0.3,
                "backgroundColor": "rgba(78, 115, 223, 0.05)",
                "borderColor": "rgba(78, 115, 223, 1)",
                "pointRadius": 3,
                "pointBackgroundColor": "rgba(78, 115, 223, 1)",
                "pointBorderColor": "rgba(78, 115, 223, 1)",
                "pointHoverRadius": 3,
                "pointHoverBackgroundColor": "rgba(78, 115, 223, 1)",
                "pointHoverBorderColor": "rgba(78, 115, 223, 1)",
                "pointHitRadius": 10,
                "pointBorderWidth": 2,
                "data": numbers,
            }],
        },

    })


@login_required
def bar_chart(request):
    transactions = Transaction.objects.filter(created_at__year=2024)
    grouped  = transactions.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    numbers = []
    months = []
    for i in grouped:
        numbers.append(i['count'])
        months.append(i['month'].strftime('%b'))
    print(months)
    return JsonResponse({
        "title": "Transactions Grouped By Month",
        "data": {
            "labels": months,
            "datasets": [{
                "label": "Total",
                "backgroundColor": "#4e73df",
                "hoverBackgroundColor": "#2e59d9",
                "borderColor": "#4e73df",
                "data": numbers,
            }],
        },
    })


def login_page(request):
    if request.method == "GET":
       return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('dashboard')
        messages.warning(request, 'Invalid username or password!')
        return redirect('login')
@login_required
def logout_page(request):
    logout(request)
    return redirect('login')

@login_required
@permission_required("main.lost_book", raise_exception=True)
def lost_book(request, id):
    transactions = Transaction.objects.get(id=id)
    transactions.status = 'LOST'
    transactions.return_date = date.today()
    transactions.save()
    messages.error(request, 'Book registered as lost!')
    return redirect('borrowed_books')