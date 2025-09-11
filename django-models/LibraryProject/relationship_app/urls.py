from django.urls import path
from . import views
from .views import LibraryDetailView

urlpatterns = [
    # Function-based view for books
    path('books/', views.list_books, name='list_books'),

    # Class-based view for library details
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # User authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
