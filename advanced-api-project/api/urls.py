from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    
    # Book ListView - for retrieving all books
    path('books/', views.BookListView.as_view(), name='book-list'),
    
    # Book CreateView - for adding a new book
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    
    # Book DetailView - for retrieving a single book by ID
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # Book UpdateView - for modifying an existing book
    path('books/update/<int:pk>/', views.BookUpdateView.as_view(), name='book-update'),
    
    # Book DeleteView - for removing a book
    path('books/delete/<int:pk>/', views.BookDeleteView.as_view(), name='book-delete'),
    
    
    # Author ListView
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    
    # Author CreateView
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    
    # Author DetailView
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    
    # Author UpdateView
    path('authors/update/<int:pk>/', views.AuthorUpdateView.as_view(), name='author-update'),
    
    # Author DeleteView
    path('authors/delete/<int:pk>/', views.AuthorDeleteView.as_view(), name='author-delete'),
]