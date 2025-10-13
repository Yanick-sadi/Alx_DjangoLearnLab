from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class BookListView(generics.ListAPIView):
   
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow read for anyone, write for authenticated
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']  # Default ordering

    def get_queryset(self):
        """
        Customize queryset to optionally filter by author if provided in query params.
        """
        queryset = super().get_queryset()
        author_id = self.request.query_params.get('author_id')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        return queryset


class BookDetailView(generics.RetrieveAPIView):
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'


class BookCreateView(generics.CreateAPIView):
   
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create

    def perform_create(self, serializer):
        """
        Custom method called when creating a new book instance.
        Can be used to add additional logic before saving.
        """
        serializer.save()
        # Additional logic can be added here (e.g., logging, notifications)

    def create(self, request, *args, **kwargs):
        """
        Override create method to customize response.
        """
        response = super().create(request, *args, **kwargs)
        # Add custom response data
        response.data['message'] = 'Book created successfully'
        response.data['status'] = 'success'
        return response


class BookUpdateView(generics.UpdateAPIView):
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can update
    lookup_field = 'pk'

    def perform_update(self, serializer):
        """
        Custom method called when updating a book instance.
        """
        serializer.save()

    def update(self, request, *args, **kwargs):
        """
        Override update method to customize response.
        """
        response = super().update(request, *args, **kwargs)
        response.data['message'] = 'Book updated successfully'
        response.data['status'] = 'success'
        return response


class BookDeleteView(generics.DestroyAPIView):
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can delete
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
      
        instance = self.get_object()
        book_title = instance.title
        self.perform_destroy(instance)
        return Response({
            'message': f'Book "{book_title}" deleted successfully',
            'status': 'success'
        }, status=status.HTTP_200_OK)

class AuthorListView(generics.ListAPIView):
    
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class AuthorDetailView(generics.RetrieveAPIView):
    
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'


class AuthorCreateView(generics.CreateAPIView):
   
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = 'Author created successfully'
        response.data['status'] = 'success'
        return response


class AuthorUpdateView(generics.UpdateAPIView):
    
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can update
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data['message'] = 'Author updated successfully'
        response.data['status'] = 'success'
        return response


class AuthorDeleteView(generics.DestroyAPIView):
    
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can delete
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        author_name = instance.name
        self.perform_destroy(instance)
        return Response({
            'message': f'Author "{author_name}" deleted successfully',
            'status': 'success'
        }, status=status.HTTP_200_OK)