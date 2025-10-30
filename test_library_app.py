#!/usr/bin/env python
"""
Comprehensive test script for Library Management System
Tests all major features including authentication, book management, transactions, and charts
"""
import requests
from datetime import date, timedelta

BASE_URL = "http://127.0.0.1:8000"

class LibraryAppTester:
    def __init__(self):
        self.session = requests.Session()
        self.csrf_token = None
        
    def get_csrf_token(self, url):
        """Extract CSRF token from a page"""
        response = self.session.get(url)
        if 'csrftoken' in self.session.cookies:
            return self.session.cookies['csrftoken']
        # Try to extract from HTML
        import re
        match = re.search(r'csrfmiddlewaretoken["\s]+value="([^"]+)"', response.text)
        if match:
            return match.group(1)
        return None
    
    def test_login_page(self):
        """Test if login page loads"""
        print("\n=== Testing Login Page ===")
        try:
            response = self.session.get(f"{BASE_URL}/login")
            if response.status_code == 200:
                print("✓ Login page loads successfully")
                print(f"  Status Code: {response.status_code}")
                return True
            else:
                print(f"✗ Login page failed with status: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Error loading login page: {e}")
            return False
    
    def test_login(self, username="alaty", password="admin"):
        """Test user login"""
        print(f"\n=== Testing Login (username: {username}) ===")
        try:
            # Get CSRF token
            csrf_token = self.get_csrf_token(f"{BASE_URL}/login")
            
            # Attempt login
            login_data = {
                'username': username,
                'password': password,
                'csrfmiddlewaretoken': csrf_token
            }
            
            response = self.session.post(
                f"{BASE_URL}/login",
                data=login_data,
                headers={'Referer': f"{BASE_URL}/login"}
            )
            
            # Check if redirected to dashboard
            if response.url.endswith('/') or 'dashboard' in response.url:
                print("✓ Login successful - redirected to dashboard")
                return True
            else:
                print(f"✗ Login failed - redirected to: {response.url}")
                return False
        except Exception as e:
            print(f"✗ Error during login: {e}")
            return False
    
    def test_dashboard(self):
        """Test dashboard access"""
        print("\n=== Testing Dashboard ===")
        try:
            response = self.session.get(f"{BASE_URL}/")
            if response.status_code == 200 and 'dashboard' in response.text.lower():
                print("✓ Dashboard loads successfully")
                print(f"  Status Code: {response.status_code}")
                return True
            else:
                print(f"✗ Dashboard failed with status: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Error loading dashboard: {e}")
            return False
    
    def test_books_page(self):
        """Test books in store page"""
        print("\n=== Testing Books in Store Page ===")
        try:
            response = self.session.get(f"{BASE_URL}/books")
            if response.status_code == 200:
                print("✓ Books page loads successfully")
                print(f"  Status Code: {response.status_code}")
                # Check if books are displayed
                if 'book' in response.text.lower():
                    print("  ✓ Books data is present")
                return True
            else:
                print(f"✗ Books page failed with status: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Error loading books page: {e}")
            return False
    
    def test_borrowed_books_page(self):
        """Test borrowed books page"""
        print("\n=== Testing Borrowed Books Page ===")
        try:
            response = self.session.get(f"{BASE_URL}/borrowed/books")
            if response.status_code == 200:
                print("✓ Borrowed books page loads successfully")
                print(f"  Status Code: {response.status_code}")
                return True
            else:
                print(f"✗ Borrowed books page failed with status: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Error loading borrowed books page: {e}")
            return False
    
    def test_fines_page(self):
        """Test book fines page"""
        print("\n=== Testing Book Fines Page ===")
        try:
            response = self.session.get(f"{BASE_URL}/fines")
            if response.status_code == 200:
                print("✓ Fines page loads successfully")
                print(f"  Status Code: {response.status_code}")
                return True
            else:
                print(f"✗ Fines page failed with status: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Error loading fines page: {e}")
            return False
    
    def test_pie_chart_api(self):
        """Test pie chart data API"""
        print("\n=== Testing Pie Chart API ===")
        try:
            response = self.session.get(f"{BASE_URL}/pie-chart")
            if response.status_code == 200:
                data = response.json()
                print("✓ Pie chart API works")
                print(f"  Title: {data.get('title')}")
                print(f"  Labels: {data.get('data', {}).get('labels')}")
                return True
            else:
                print(f"✗ Pie chart API failed with status: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Error calling pie chart API: {e}")
            return False
    
    def test_line_chart_api(self):
        """Test line chart data API"""
        print("\n=== Testing Line Chart API ===")
        try:
            response = self.session.get(f"{BASE_URL}/line-chart")
            if response.status_code == 200:
                data = response.json()
                print("✓ Line chart API works")
                print(f"  Title: {data.get('title')}")
                print(f"  Labels: {data.get('data', {}).get('labels')}")
                return True
            else:
                print(f"✗ Line chart API failed with status: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Error calling line chart API: {e}")
            return False
    
    def test_bar_chart_api(self):
        """Test bar chart data API"""
        print("\n=== Testing Bar Chart API ===")
        try:
            response = self.session.get(f"{BASE_URL}/bar-chart")
            if response.status_code == 200:
                data = response.json()
                print("✓ Bar chart API works")
                print(f"  Title: {data.get('title')}")
                print(f"  Labels: {data.get('data', {}).get('labels')}")
                return True
            else:
                print(f"✗ Bar chart API failed with status: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Error calling bar chart API: {e}")
            return False
    
    def test_database_data(self):
        """Test database has data"""
        print("\n=== Testing Database Data ===")
        try:
            import os
            import sys
            import django
            
            # Setup Django
            sys.path.insert(0, os.path.dirname(__file__))
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
            django.setup()
            
            from main.models import Book, Student, Transaction
            
            books_count = Book.objects.count()
            students_count = Student.objects.count()
            transactions_count = Transaction.objects.count()
            
            print(f"✓ Database connection successful")
            print(f"  Books: {books_count}")
            print(f"  Students: {students_count}")
            print(f"  Transactions: {transactions_count}")
            
            if books_count > 0 and students_count > 0:
                print("✓ Database has test data")
                return True
            else:
                print("⚠ Database is empty")
                return False
        except Exception as e:
            print(f"✗ Error checking database: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("=" * 60)
        print("LIBRARY MANAGEMENT SYSTEM - COMPREHENSIVE TEST")
        print("=" * 60)
        
        results = []
        
        # Test database first
        results.append(("Database Data", self.test_database_data()))
        
        # Test pages without authentication
        results.append(("Login Page", self.test_login_page()))
        
        # Test authentication
        results.append(("User Login", self.test_login()))
        
        # Test authenticated pages
        results.append(("Dashboard", self.test_dashboard()))
        results.append(("Books Page", self.test_books_page()))
        results.append(("Borrowed Books", self.test_borrowed_books_page()))
        results.append(("Fines Page", self.test_fines_page()))
        
        # Test API endpoints
        results.append(("Pie Chart API", self.test_pie_chart_api()))
        results.append(("Line Chart API", self.test_line_chart_api()))
        results.append(("Bar Chart API", self.test_bar_chart_api()))
        
        # Print summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"{status:8} | {test_name}")
        
        print("=" * 60)
        print(f"Results: {passed}/{total} tests passed ({passed*100//total}%)")
        print("=" * 60)
        
        return passed == total

if __name__ == "__main__":
    tester = LibraryAppTester()
    success = tester.run_all_tests()
    exit(0 if success else 1)
