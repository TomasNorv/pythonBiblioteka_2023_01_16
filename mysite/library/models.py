from django.db import models
import uuid
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Genre(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=200,
                            help_text='Įveskite knygos žanrą (pvz. detektyvas)')

    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name = "Žanras"
        verbose_name_plural ='Žanrai'


class Book(models.Model):
    title = models.CharField(verbose_name="Pavadinimas", max_length=200)
    summary = models.TextField(verbose_name="Aprasymas", max_length=1000)
    isbn = models.CharField(verbose_name="ISBN", max_length=13,
                            help_text='13 Simbolių <a href="https://www.isbn-international.org/content/what-isbn">ISBN kodas</a>')
    author = models.ForeignKey(to="Author", on_delete=models.SET_NULL, null=True, related_name="books") #related_name kad tureti rysi su knygom autoriui.
    genre = models.ManyToManyField(to="Genre")
    cover = models.ImageField(verbose_name='Viršelis', upload_to='covers', null=True, blank=True)
    def display_genre(self):   #arba  return ', '.join(genre.name for genre in self.genre.all()[:3])
        sujungta= ""
        zanrai = self.genre.all()
        for zanras in zanrai:
            sujungta += zanras.name + ", "
        return sujungta
    display_genre.short_description ="Žanrai"  # pakeitem pavadinima is display genre i Žanrai

    def __str__(self):
        return f"{self.title} {self.author}"

    class Meta:
        verbose_name = "Knyga"
        verbose_name_plural ='Knygos'


class Author(models.Model):
    first_name = models.CharField('Vardas', max_length=100)
    last_name = models.CharField('Pavardė', max_length=100)
    description = models.TextField(verbose_name="Aprašymas", max_length=3000, null=True, blank=True, default="")

    def display_books(self):
        return ", ".join(book.title for book in self.books.all()[:3])

    display_books.short_description = "Knygos"



    def __str__(self):
        return f"{self.first_name}  {self.last_name}"

    class Meta:
        verbose_name = "Autorius"
        verbose_name_plural ='Autoriai'


class BookInstance(models.Model):
    book = models.ForeignKey(to="Book", on_delete=models.CASCADE, related_name='instances')
    uuid = models.UUIDField(verbose_name="UUID", default=uuid.uuid4, help_text='Unikalus ID knygos kopijai')
    due_back = models.DateField('Bus prieinama', null=True, blank=True)
    reader = models.ForeignKey(to=User, verbose_name="Skaitytojas",  on_delete=models.SET_NULL, null=True, blank=True)

    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False



    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Statusas',
    )


    def __str__(self):
        return f"{self.book} - {self.uuid}"

    class Meta:
        verbose_name = "Knygos egzempliorius"
        verbose_name_plural ='Knygų egzemplioriai'


