from django.shortcuts import render, get_object_or_404
from django.db.models import Min, Max
from .models import Book
from datetime import datetime


def books_view(request):
    """Отображает все книги."""
    books = Book.objects.all().order_by('pub_date')
    context = {'books': books}
    return render(request, 'books/books_list.html', context)


def book_by_date(request, pub_date):
    """Отображает книги за указанную дату и ссылки на соседние даты."""
    try:
        pub_date = datetime.strptime(pub_date, '%Y-%m-%d').date()
    except ValueError:
        from django.http import Http404
        raise Http404("Неверный формат даты")
    books = Book.objects.filter(pub_date=pub_date)
    if not books.exists():
        from django.http import Http404
        raise Http404("Книг за эту дату не найдено")
    dates = Book.objects.dates('pub_date', 'day', order='ASC')
    dates_list = list(dates)
    prev_date = None
    next_date = None
    try:
        current_index = dates_list.index(pub_date)
        if current_index > 0:
            prev_date = dates_list[current_index - 1]
        if current_index < len(dates_list) - 1:
            next_date = dates_list[current_index + 1]
    except ValueError:
        pass
    context = {
        'books': books,
        'pub_date': pub_date,
        'prev_date': prev_date,
        'next_date': next_date,
    }
    return render(request, 'books/book_by_date.html', context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/book_detail.html', {'book': book})