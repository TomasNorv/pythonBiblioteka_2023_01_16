from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse
from .models import Book, BookInstance, Author
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.generic.edit import FormMixin
from .forms import BookReviewForm, UserUpdateForm, ProfilisUpdateForm, UserCreateForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

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





class BookDetailView(FormMixin, generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'book.html'
    form_class = BookReviewForm


    def get_success_url(self):
        return reverse('book', kwargs={'pk': self.object.id})  # nurodome, kur atsidursime komentaro sėkmės atveju.

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.book = self.object  # štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
        form.instance.reviewer = self.request.user
        form.save()
        return super(BookDetailView, self).form_valid(form)

def search(request):
    query = request.GET.get('query')
    search_results = Book.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query) | Q(author__first_name__icontains=query) | Q(author__last_name__icontains=query))
    return render(request, 'search.html', {'books': search_results, 'query': query})


class UserBookListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    paginate_by = 3
    template_name = 'user_books.html'
    context_object_name = 'instances'

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user)
class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = BookInstance
    template_name = 'user_book.html'
    context_object_name = 'instance'

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = BookInstance
    #fields = ['book', 'due_back', 'status']
    success_url = "/library/userbooks/"
    template_name = 'user_bookinstance_form.html'
    form_class = UserUpdateForm

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

    def test_func(self):
        bookinstance = self.get_object()
        return self.request.user == bookinstance.reader



class UserCreateView(LoginRequiredMixin, generic.CreateView):
    model = BookInstance
    #fields = ['book', 'due_back', 'status']
    success_url = "/library/userbooks/"
    template_name = 'user_bookinstance_form.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = BookInstance
    success_url = "/library/userbooks/"
    template_name = 'user_bookinstance_delete.html'
    context_object_name = 'instance'

    def test_func(self):
        bookinstance = self.get_object()
        return self.request.user == bookinstance.reader



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
                #messages.error(request, f'Vartotojo vardas {username} užimtas!')
                messages.error(request, _('Username %s already exists!') % username)
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    #messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    messages.error(request, _('Email %s already exists!') % email)
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    #messages.info(request, (f'Vartotojas {username} užregistruotas!')
                    messages.info(request, _('User %s  registered!') % username)
                    return redirect('login')
        else:
            #messages.error(request, ('Slaptažodžiai nesutampa!')
            messages.error(request, _('Passwords do not match!'))
            return redirect('register')
    return render(request, 'registration/register.html')

@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profilis.html', context=context)



