# M-Pesa Payment Integration Guide

## Current Implementation in Library Management System

### Overview
The current implementation uses `django-daraja` to integrate M-Pesa's Daraja API for handling payments. The system is configured for a library management context where payments are typically for membership fees, book fines, or service charges.

### Key Components

1. **Configuration**
   - Uses `python-decouple` for environment variables
   - M-Pesa credentials stored in `.env` file
   - Sandbox environment for testing

2. **Payment Flow**
   ```mermaid
   sequenceDiagram
       User->>+Django: Initiate Payment
       Django->>+M-Pesa API: STK Push Request
       M-Pesa API->>+User's Phone: STK Push Notification
       User->>+M-Pesa: Enter M-Pesa PIN
       M-Pesa->>+M-Pesa API: Payment Confirmation
       M-Pesa API->>+Django: Callback with Payment Status
       Django->>+Database: Update Payment Status
   ```

3. **Implementation Details**
   - Uses M-Pesa Express (STK Push)
   - Payment amounts are typically fixed or calculated by the system
   - Single payment recipient (the library)
   - Simple product/service description

## E-commerce Implementation Differences

### 1. Dynamic Payment Amounts
- **Current**: Fixed or system-calculated amounts
- **E-commerce**: Variable amounts based on cart contents
- **Implementation**: Calculate total dynamically from shopping cart

### 2. Multiple Payment Recipients
- **Current**: Single business shortcode
- **E-commerce**: May need multi-vendor support
- **Implementation**: Track payments per vendor and handle splitting

### 3. Payment Verification
- **Current**: Simple status updates
- **E-commerce**: Complex order status management
- **Implementation**: Robust webhook handling for payment confirmations

### 4. Refund Processing
- **Current**: Manual or non-existent
- **E-commerce**: Automated refund system required
- **Implementation**: M-Pesa B2C API integration

### 5. Transaction Records
- **Current**: Basic payment logging
- **E-commerce**: Detailed transaction history
- **Implementation**: Enhanced transaction model with relationships to orders

## Implementation Guide for E-commerce

### 1. Enhanced Models
```python
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    order_number = models.CharField(max_length=32, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    mpesa_receipt = models.CharField(max_length=100, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
```

### 2. Payment Processing
```python
def initiate_stk_push(order):
    from django_daraja.mpesa.core import MpesaClient
    
    cl = MpesaClient()
    phone_number = order.user.profile.phone_number
    amount = int(order.total_amount)
    account_reference = order.order_number
    transaction_desc = f"Payment for order {order.order_number}"
    
    response = cl.stk_push(
        phone_number,
        amount,
        account_reference,
        transaction_desc,
        callback_url=settings.MPESA_CALLBACK_URL
    )
    return response
```

### 3. Callback Handler
```python
@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result_code = data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
        
        if result_code == 0:
            # Payment successful
            metadata = data['Body']['stkCallback']['CallbackMetadata']['Item']
            receipt_number = next(item['Value'] for item in metadata if item['Name'] == 'MpesaReceiptNumber')
            order_number = next(item['Value'] for item in metadata if item['Name'] == 'AccountReference')
            
            order = Order.objects.get(order_number=order_number)
            order.mpesa_receipt = receipt_number
            order.payment_status = 'COMPLETED'
            order.save()
            
            # Additional order processing (inventory, notifications, etc.)
            process_successful_order(order)
    
    return JsonResponse({'status': 'success'})
```

## Security Considerations

1. **Sensitive Data**
   - Never store M-Pesa API keys in version control
   - Use environment variables for all credentials
   
2. **Data Validation**
   - Validate all user inputs
   - Sanitize callback data
   
3. **Rate Limiting**
   - Implement rate limiting on payment endpoints
   - Prevent duplicate transactions

## Testing

1. **Sandbox Environment**
   - Use M-Pesa sandbox for development
   - Test with test credentials
   
2. **Test Cases**
   - Successful payments
   - Failed payments
   - Timeout scenarios
   - Duplicate payment attempts

## Deployment

1. **Production Credentials**
   - Obtain production credentials from Safaricom
   - Update environment variables
   
2. **Webhook Configuration**
   - Set up HTTPS endpoints
   - Configure webhook URLs in M-Pesa portal

## Support
For any issues, refer to:
- [M-Pesa Daraja API Documentation](https://developer.safaricom.co.ke/)
- [django-daraja Documentation](https://github.com/ngamita/django-daraja)

---
*Documentation last updated: January 2026*
