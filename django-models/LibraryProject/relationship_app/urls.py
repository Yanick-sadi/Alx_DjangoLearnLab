from django.urls import path
from . import views
from .views import LibraryDetailView

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),  # include app URLs
]
urlpatterns = [
    # Function-based view: list all books
    path("books/", views.list_books, name="list_books"),

    # Class-based view: detail for a specific library
    # Example URL: /libraries/1/
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
]