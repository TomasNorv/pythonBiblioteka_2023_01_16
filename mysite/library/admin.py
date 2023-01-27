from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, BookReview

class BookInstanceInLine(admin.TabularInline):
    model = BookInstance
    readonly_fields = ['uuid'] # uzdejom apsibojima kad nebutu galima redaguoti uuid
   #can_delete = False          # uzdejom apribojima kad nebutu galima istrinti (situ atveju tas netinka)
    extra = 0                   # išjungia papildomas tuščias eilutes įvedimui


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'display_genre')
    inlines = [BookInstanceInLine]
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'reader') # padarem stulpelius, atvaizduoja stulpelius
    list_filter = ('status', 'due_back')   #uzdejom piltra
    search_fields = ("uuid", "book__title") #pridejom paieska pagal uuid ir knygos pavadinima
    list_editable = ('due_back', 'status', 'reader')
    # fieldsets = (
    #     ('General', {'fields': ('uuid', 'book')}),
    #     ('Availability', {'fields': ('status', 'due_back', 'reader')}),
    # )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'display_books']

class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'date_created', 'reviewer', 'content')

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(BookReview, BookReviewAdmin)
