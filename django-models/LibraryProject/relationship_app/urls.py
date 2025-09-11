from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import LibraryDetailView

urlpatterns = [
    # Function-based view for books
    path('books/', views.list_books, name='list_books'),

    # Class-based view for library details
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Authentication using class-based views
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register_view, name='register'),  # registration remains function-based
]