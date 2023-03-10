from django.urls import path, include
from. import views
urlpatterns = [
    path('', views.index, name= "index"),
    path('authors/',views.authors, name = "authors"),
    path('authors/<int:author_id>',views.author, name='author'),
    path("books/", views.BookListView.as_view(), name="books"),
    path("books/<int:pk>", views.BookDetailView.as_view(), name ="book"),
    path("search", views.search, name="search"),
    path('userbooks/', views.UserBookListView.as_view(), name='user_books'),
    path('userbooks/<int:pk>', views.UserDetailView.as_view(), name= 'user_book'),
    path('userbooks/cerate', views.UserCreateView.as_view(), name= 'user_bookinstance_create'),
    path('register/', views.register, name='register'),
    path('profilis/', views.profilis, name='profilis'),
    path('userbooks/<int:pk>/update', views.UserUpdateView.as_view(), name="user_bookinstance_update"),
    path('userbooks/<int:pk>/delete', views.UserDeleteView.as_view(), name="user_bookinstance_delete"),
    path('i18n/', include('django.conf.urls.i18n')),

]