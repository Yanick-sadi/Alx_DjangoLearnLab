from django.urls import path
from .views import BookListCreateView, BookDetailView
from django.contrib import admin
from django.urls import path, include
from .views import BookList

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), 
    path('books/', BookList.as_view(), name='book-list'),

]


