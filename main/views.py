from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')


def books_in_store(request):
    return render(request, 'books_in_store.html')


def borrowed_books(request):
    return render(request, 'borrowed_books.html')


def book_fines(request):
    return render(request, 'book_fines.html')


def issue_book(request):
    return None