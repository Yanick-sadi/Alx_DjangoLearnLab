from django.urls import path
from .views import BookListCreateView, BookDetailView
from django.contrib import admin
from django.urls import path, include
from .views import BookList
from .views import BookViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), 
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),

]


