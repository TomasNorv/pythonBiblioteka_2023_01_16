from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book, BookInstance, Author
from django.views import generic
# Create your views here.


def index(request):
    num_books = Book.objects.all().count()       # Suskaičiuokime keletą pagrindinių objektų
    num_instances = BookInstance.objects.all().count() # Suskaičiuokime keletą pagrindinių objektų
    num_instances_available = BookInstance.objects.filter(status__exact='g').count() # Laisvos knygos (tos, kurios turi statusą 'g')
    num_authors = Author.objects.count()    # Kiek yra autorių

    # perduodame informaciją į šabloną žodyno(dictionary) pavidale:
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # renderiname index.html, su duomenimis kintamąjame context
    return render(request, 'index.html', context = context)

def authors(request):
    authors = Author.objects.all()
    context = {
        'authors': authors,
    }
    return render(request, 'authors.html', context = context)

def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    context = {
        'author': author,
    }
    return render(request, 'author.html', context=context)

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'books.html'

class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'book.html'
