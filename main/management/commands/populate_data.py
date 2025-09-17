from django.core.management.base import BaseCommand
from main.models import Book, Student, Transaction
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        # Sample book data
        books_data = [
            {"title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960, "subject": "Literature", "isbn": "9780061120084"},
            {"title": "1984", "author": "George Orwell", "year": 1949, "subject": "Literature", "isbn": "9780547928227"},
            {"title": "Pride and Prejudice", "author": "Jane Austen", "year": 1813, "subject": "Literature", "isbn": "9780141439518"},
            {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925, "subject": "Literature", "isbn": "9780743273565"},
            {"title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling", "year": 1997, "subject": "Fantasy", "isbn": "9780747532699"},
            {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "year": 1951, "subject": "Literature", "isbn": "9780316769174"},
            {"title": "Lord of the Flies", "author": "William Golding", "year": 1954, "subject": "Literature", "isbn": "9780571056866"},
            {"title": "The Chronicles of Narnia", "author": "C.S. Lewis", "year": 1950, "subject": "Fantasy", "isbn": "9780066238500"},
            {"title": "Animal Farm", "author": "George Orwell", "year": 1945, "subject": "Literature", "isbn": "9780451526342"},
            {"title": "Brave New World", "author": "Aldous Huxley", "year": 1932, "subject": "Science Fiction", "isbn": "9780060850524"},
            {"title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937, "subject": "Fantasy", "isbn": "9780547928227"},
            {"title": "Jane Eyre", "author": "Charlotte Bronte", "year": 1847, "subject": "Literature", "isbn": "9780141441146"},
            {"title": "Wuthering Heights", "author": "Emily Bronte", "year": 1847, "subject": "Literature", "isbn": "9780141439556"},
            {"title": "Great Expectations", "author": "Charles Dickens", "year": 1861, "subject": "Literature", "isbn": "9780141439563"},
            {"title": "The Picture of Dorian Gray", "author": "Oscar Wilde", "year": 1890, "subject": "Literature", "isbn": "9780141439570"},
            {"title": "Fahrenheit 451", "author": "Ray Bradbury", "year": 1953, "subject": "Science Fiction", "isbn": "9781451673319"},
            {"title": "Of Mice and Men", "author": "John Steinbeck", "year": 1937, "subject": "Literature", "isbn": "9780140177398"},
            {"title": "The Grapes of Wrath", "author": "John Steinbeck", "year": 1939, "subject": "Literature", "isbn": "9780143039433"},
            {"title": "Romeo and Juliet", "author": "William Shakespeare", "year": 1597, "subject": "Drama", "isbn": "9780743477116"},
            {"title": "Hamlet", "author": "William Shakespeare", "year": 1603, "subject": "Drama", "isbn": "9780743477123"},
            {"title": "Macbeth", "author": "William Shakespeare", "year": 1623, "subject": "Drama", "isbn": "9780743477130"},
            {"title": "A Midsummer Night's Dream", "author": "William Shakespeare", "year": 1600, "subject": "Drama", "isbn": "9780743477147"},
            {"title": "The Merchant of Venice", "author": "William Shakespeare", "year": 1605, "subject": "Drama", "isbn": "9780743477154"},
            {"title": "Introduction to Algorithms", "author": "Thomas H. Cormen", "year": 2009, "subject": "Computer Science", "isbn": "9780262033848"},
            {"title": "Clean Code", "author": "Robert C. Martin", "year": 2008, "subject": "Computer Science", "isbn": "9780132350884"},
            {"title": "Design Patterns", "author": "Gang of Four", "year": 1994, "subject": "Computer Science", "isbn": "9780201633612"},
            {"title": "The Pragmatic Programmer", "author": "David Thomas", "year": 1999, "subject": "Computer Science", "isbn": "9780201616224"},
            {"title": "Structure and Interpretation of Computer Programs", "author": "Harold Abelson", "year": 1985, "subject": "Computer Science", "isbn": "9780262510875"},
            {"title": "Calculus: Early Transcendentals", "author": "James Stewart", "year": 2015, "subject": "Mathematics", "isbn": "9781285741550"},
            {"title": "Linear Algebra and Its Applications", "author": "Gilbert Strang", "year": 2016, "subject": "Mathematics", "isbn": "9781285463247"},
        ]

        # Sample student data
        students_data = [
            {"name": "Alice Johnson", "email": "alice.johnson@example.com", "phone": "0712345678", "adm_no": "STU001"},
            {"name": "Bob Smith", "email": "bob.smith@example.com", "phone": "0723456789", "adm_no": "STU002"},
            {"name": "Carol Williams", "email": "carol.williams@example.com", "phone": "0734567890", "adm_no": "STU003"},
            {"name": "David Brown", "email": "david.brown@example.com", "phone": "0745678901", "adm_no": "STU004"},
            {"name": "Eve Davis", "email": "eve.davis@example.com", "phone": "0756789012", "adm_no": "STU005"},
            {"name": "Frank Miller", "email": "frank.miller@example.com", "phone": "0767890123", "adm_no": "STU006"},
            {"name": "Grace Wilson", "email": "grace.wilson@example.com", "phone": "0778901234", "adm_no": "STU007"},
            {"name": "Henry Moore", "email": "henry.moore@example.com", "phone": "0789012345", "adm_no": "STU008"},
            {"name": "Ivy Taylor", "email": "ivy.taylor@example.com", "phone": "0790123456", "adm_no": "STU009"},
            {"name": "Jack Anderson", "email": "jack.anderson@example.com", "phone": "0701234567", "adm_no": "STU010"},
            {"name": "Kate Thomas", "email": "kate.thomas@example.com", "phone": "0712345679", "adm_no": "STU011"},
            {"name": "Liam Jackson", "email": "liam.jackson@example.com", "phone": "0723456780", "adm_no": "STU012"},
            {"name": "Mia White", "email": "mia.white@example.com", "phone": "0734567891", "adm_no": "STU013"},
            {"name": "Noah Harris", "email": "noah.harris@example.com", "phone": "0745678902", "adm_no": "STU014"},
            {"name": "Olivia Martin", "email": "olivia.martin@example.com", "phone": "0756789013", "adm_no": "STU015"},
        ]

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Transaction.objects.all().delete()
        Book.objects.all().delete()
        Student.objects.all().delete()

        # Create books
        self.stdout.write('Creating books...')
        books = []
        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults=book_data
            )
            books.append(book)
            if created:
                self.stdout.write(f'Created book: {book.title}')

        # Create students
        self.stdout.write('Creating students...')
        students = []
        for student_data in students_data:
            student, created = Student.objects.get_or_create(
                adm_no=student_data['adm_no'],
                defaults=student_data
            )
            students.append(student)
            if created:
                self.stdout.write(f'Created student: {student.name}')

        # Create some transactions
        self.stdout.write('Creating transactions...')
        statuses = ['BORROWED', 'RETURNED', 'LOST']
        
        for i in range(20):  # Create 20 random transactions
            book = random.choice(books)
            student = random.choice(students)
            status = random.choice(statuses)
            
            # Random dates
            start_date = datetime.now() - timedelta(days=random.randint(1, 60))
            expected_return = start_date + timedelta(days=14)  # 2 weeks loan period
            
            return_date = None
            if status == 'RETURNED':
                # Some returned on time, some late
                return_date = expected_return + timedelta(days=random.randint(-3, 10))
            elif status == 'LOST':
                return_date = expected_return + timedelta(days=random.randint(15, 30))
            
            transaction = Transaction.objects.create(
                book=book,
                student=student,
                status=status,
                expected_return_date=expected_return.date(),
                return_date=return_date.date() if return_date else None,
                created_at=start_date
            )
            
            self.stdout.write(f'Created transaction: {book.title} -> {student.name} ({status})')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(books)} books, {len(students)} students, and 20 transactions!'
            )
        )