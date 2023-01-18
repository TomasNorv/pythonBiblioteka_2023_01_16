from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'display_genre')


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance)