from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ListAPIView

class BookList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
