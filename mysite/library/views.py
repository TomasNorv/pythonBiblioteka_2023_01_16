from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book, BookInstance, Author
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.forms import User

# Create your views here.


def index(request):
    num_books = Book.objects.all().count()       # Suskaičiuokime keletą pagrindinių objektų
    num_instances = BookInstance.objects.all().count() # Suskaičiuokime keletą pagrindinių objektų
    num_instances_available = BookInstance.objects.filter(status__exact='g').count() # Laisvos knygos (tos, kurios turi statusą 'g')
    num_authors = Author.objects.count()    # Kiek yra autorių

    # perduodame informaciją į šabloną žodyno(dictionary) pavidale:
    num_visits = request.session.get('num_visits', 1) # pridejom funkcija kad matytumem apsilankymu kieki puslapyje
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # renderiname index.html, su duomenimis kintamąjame context
    return render(request, 'index.html', context = context)

def authors(request):
    paginator = Paginator(Author.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    context = {
        'authors': paged_authors,
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
    paginate_by = 3
    context_object_name = 'books'
    template_name = 'books.html'

class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'book.html'

def search(request):
    query = request.GET.get('query')
    search_results = Book.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query) | Q(author__first_name__icontains=query) | Q(author__last_name__icontains=query))
    return render(request, 'search.html', {'books': search_results, 'query': query})


class UserBookListView(generic.ListView, LoginRequiredMixin):
    model = BookInstance
    paginate_by = 3
    template_name = 'user_books.html'
    context_object_name = 'instances'

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user)


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')


