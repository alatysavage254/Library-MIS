# Library Management System

A comprehensive Django-based Library Management System with M-Pesa payment integration, designed to manage books, students, transactions, and fines efficiently.

## Features

- **Book Management**: Add, edit, delete, and search books with ISBN, title, author, and availability tracking
- **Student Management**: Register and manage student accounts with admission numbers
- **Transaction Tracking**: Issue and return books with automated fine calculations
- **Payment Integration**: M-Pesa payment gateway for fine payments
- **Dashboard Analytics**: Visual charts and statistics for library operations
- **Admin Panel**: Full Django admin interface for system management

## Technologies Used

- **Backend**: Django 5.1.3
- **Database**: MySQL/MariaDB
- **Payment Gateway**: M-Pesa (django-daraja)
- **Frontend**: Bootstrap 4, SB Admin 2 theme
- **Charts**: Chart.js for analytics
- **Authentication**: Django built-in authentication system

## Prerequisites

- Python 3.8+
- MySQL/MariaDB
- Virtual environment (recommended)

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/alatysavage254/Library-MIS.git
   cd Library-MIS
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   - Create a MySQL database named `library_db`
   - Create a MySQL user `django_user` with password `your_password`
   - Grant all privileges on `library_db` to `django_user`

5. **Configure Settings**
   - Update database credentials in `library_project/settings.py`
   - Configure M-Pesa credentials for payment integration

6. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Populate Sample Data (Optional)**
   ```bash
   python manage.py populate_data
   ```

9. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

10. **Access the Application**
    - Main Application: http://localhost:8000/
    - Admin Panel: http://localhost:8000/admin/

## Project Structure

```
library_mis/
├── manage.py
├── requirements.txt
├── library_project/
│   ├── settings.py          # Django settings
│   ├── urls.py             # URL routing
│   └── wsgi.py
├── main/
│   ├── models.py           # Data models (Book, Student, Transaction, Payment)
│   ├── views.py            # View functions
│   ├── admin.py            # Admin configuration
│   ├── assets/             # Static files (CSS, JS, images)
│   └── migrations/
└── templates/              # HTML templates
    ├── dashboard.html
    ├── books_in_store.html
    ├── borrowed_books.html
    ├── issue.html
    └── login.html
```

## Models

### Book
- ISBN (Primary Key)
- Title
- Author
- Genre
- Publication Date
- Available Copies
- Total Copies

### Student
- Admission Number (Primary Key)
- Name
- Email
- Phone Number
- Course
- Year of Study

### Transaction
- Transaction ID
- Book (Foreign Key)
- Student (Foreign Key)
- Issue Date
- Due Date
- Return Date
- Status (Issued/Returned/Overdue)
- Fine Amount

### Payment
- Payment ID
- Transaction (Foreign Key)
- Amount
- Payment Date
- Payment Method
- M-Pesa Transaction ID

## Usage

### For Librarians

1. **Login** to the system using admin credentials
2. **Add Books** through the dashboard or admin panel
3. **Register Students** with their details
4. **Issue Books** by selecting student and book
5. **Process Returns** and calculate fines automatically
6. **View Analytics** on the dashboard for insights

### For Students

1. **View Available Books** in the catalog
2. **Check Borrowed Books** and due dates
3. **Pay Fines** using M-Pesa integration
4. **View Transaction History**

## M-Pesa Payment Integration

The system integrates with Safaricom M-Pesa for fine payments:

- Sandbox environment for testing
- Production-ready configuration
- Automatic payment verification
- Transaction logging and tracking

## Sample Data

The system includes a management command to populate sample data:

- 30 sample books across various genres
- 15 sample students
- 20 sample transactions with different statuses

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Security Features

- CSRF protection enabled
- SQL injection prevention
- Secure password hashing
- Session security
- Input validation and sanitization

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure proper database credentials
3. Set up static file serving
4. Configure M-Pesa production credentials
5. Set up SSL/HTTPS
6. Configure proper logging

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, please contact:
- Email: your-email@example.com
- GitHub Issues: [Create an issue](https://github.com/alatysavage254/Library-MIS/issues)

## Changelog

### Version 1.0.0
- Initial release
- Basic CRUD operations for books and students
- Transaction management
- M-Pesa payment integration
- Dashboard analytics
- Admin panel configuration

---

**Developed with ❤️ using Django**