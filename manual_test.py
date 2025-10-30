#!/usr/bin/env python
"""
Manual test to verify the library app is working
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()

from django.contrib.auth.models import User
from main.models import Book, Student, Transaction, Payment
from datetime import date, timedelta

print("=" * 70)
print("LIBRARY MANAGEMENT SYSTEM - MANUAL TEST")
print("=" * 70)

# Test 1: Check Users
print("\n1. USERS IN SYSTEM:")
print("-" * 70)
users = User.objects.all()
for user in users:
    print(f"   Username: {user.username:15} | Staff: {user.is_staff} | Superuser: {user.is_superuser}")

# Test 2: Check Books
print("\n2. BOOKS IN LIBRARY:")
print("-" * 70)
books = Book.objects.all()[:5]
print(f"   Total Books: {Book.objects.count()}")
print("   Sample Books:")
for book in books:
    print(f"   - {book.title[:40]:40} by {book.author[:20]:20} (ISBN: {book.isbn})")

# Test 3: Check Students
print("\n3. STUDENTS REGISTERED:")
print("-" * 70)
students = Student.objects.all()[:5]
print(f"   Total Students: {Student.objects.count()}")
print("   Sample Students:")
for student in students:
    print(f"   - {student.name[:30]:30} | Adm No: {student.adm_no:10} | Email: {student.email}")

# Test 4: Check Transactions
print("\n4. BOOK TRANSACTIONS:")
print("-" * 70)
transactions = Transaction.objects.all()[:5]
print(f"   Total Transactions: {Transaction.objects.count()}")
print("   Recent Transactions:")
for trans in transactions:
    print(f"   - {trans.book.title[:30]:30} | {trans.student.name[:20]:20} | Status: {trans.status}")

# Test 5: Check Borrowed Books
print("\n5. CURRENTLY BORROWED BOOKS:")
print("-" * 70)
borrowed = Transaction.objects.filter(status='BORROWED')
print(f"   Total Borrowed: {borrowed.count()}")
for trans in borrowed[:5]:
    days_left = (trans.expected_return_date - date.today()).days
    print(f"   - {trans.book.title[:30]:30} | Due: {trans.expected_return_date} ({days_left} days)")

# Test 6: Check Fines
print("\n6. OVERDUE BOOKS WITH FINES:")
print("-" * 70)
all_trans = Transaction.objects.all()
fines = [t for t in all_trans if t.total_fine > 0]
print(f"   Total with Fines: {len(fines)}")
for trans in fines[:5]:
    print(f"   - {trans.book.title[:30]:30} | Fine: Ksh.{trans.total_fine} ({trans.overdue_days} days)")

# Test 7: Check Payments
print("\n7. PAYMENT RECORDS:")
print("-" * 70)
payments = Payment.objects.all()[:5]
print(f"   Total Payments: {Payment.objects.count()}")
if payments:
    for payment in payments:
        print(f"   - Amount: Ksh.{payment.amount} | Status: {payment.status} | Code: {payment.code or 'N/A'}")
else:
    print("   No payments recorded yet")

# Test 8: Statistics
print("\n8. STATISTICS:")
print("-" * 70)
total_books = Book.objects.count()
total_students = Student.objects.count()
total_transactions = Transaction.objects.count()
borrowed_count = Transaction.objects.filter(status='BORROWED').count()
returned_count = Transaction.objects.filter(status='RETURNED').count()
lost_count = Transaction.objects.filter(status='LOST').count()

print(f"   Total Books:        {total_books}")
print(f"   Total Students:     {total_students}")
print(f"   Total Transactions: {total_transactions}")
print(f"   Currently Borrowed: {borrowed_count}")
print(f"   Returned:           {returned_count}")
print(f"   Lost:               {lost_count}")

# Test 9: Server Status
print("\n9. SERVER STATUS:")
print("-" * 70)
import requests
try:
    response = requests.get("http://127.0.0.1:8000/login", timeout=2)
    if response.status_code == 200:
        print("   ✓ Server is running at http://127.0.0.1:8000")
        print("   ✓ Login page is accessible")
    else:
        print(f"   ⚠ Server responded with status: {response.status_code}")
except Exception as e:
    print(f"   ✗ Server is not accessible: {e}")

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
print("\nTo access the application:")
print("1. Open your browser and go to: http://127.0.0.1:8000")
print("2. Login with username: alaty (or savage)")
print("3. You'll need the password that was set during user creation")
print("\nTo create a new superuser, run:")
print("   python manage.py createsuperuser")
print("=" * 70)
