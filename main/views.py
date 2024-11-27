from datetime import date, timedelta

from django.contrib import messages
from django.shortcuts import render, redirect

from main.models import Book, Transaction, Student


# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')


def books_in_store(request):
    books = Book.objects.all()
    return render(request, 'books_in_store.html', {'books': books})


def borrowed_books(request):
    borrowed = Transaction.objects.all()
    return render(request, 'borrowed_books.html', {"borrowed_items": borrowed})


def book_fines(request):
    return render(request, 'book_fines.html')


def issue_book(request, id):
    book = Book.objects.get(pk=id)
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


def return_book(request, id):
    transaction = Transaction.objects.get(pk=id)
    transaction.return_date = date.today()
    transaction.status = 'RETURNED'
    transaction.save()
    messages.success(request, f'Book {transaction.book.title} was returned successfully')
    if transaction.total_fine > 0:
        messages.warning(request, f'Book {transaction.book.title} has incurred a fine of Ksh.{transaction.total_fine}')
    return redirect('books_in_store')