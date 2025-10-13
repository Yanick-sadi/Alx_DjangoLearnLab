from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from rest_framework.filters import SearchFilter, OrderingFilter  # Explicit imports for both filters
from django_filters import FilterSet, CharFilter, NumberFilter
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class BookFilter(FilterSet):
    """
    Custom filter set for Book model to enable advanced filtering capabilities.
    Provides precise control over how books can be filtered via query parameters.
    """
    title = CharFilter(field_name='title', lookup_expr='icontains', 
                      help_text="Filter books by title (case-insensitive contains)")
    
    author_name = CharFilter(field_name='author__name', lookup_expr='icontains',
                           help_text="Filter books by author name (case-insensitive contains)")
    
    publication_year = NumberFilter(field_name='publication_year', 
                                   help_text="Filter books by exact publication year")
    
    publication_year_min = NumberFilter(field_name='publication_year', lookup_expr='gte',
                                      help_text="Filter books with publication year greater than or equal to")
    
    publication_year_max = NumberFilter(field_name='publication_year', lookup_expr='lte',
                                      help_text="Filter books with publication year less than or equal to")
    
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'author__name': ['exact', 'icontains'],
            'publication_year': ['exact', 'gte', 'lte'],
        }


class BookListView(generics.ListAPIView):
    """
    Enhanced ListView for retrieving all books with comprehensive filtering, 
    searching, and ordering capabilities.
    
    Features:
    - Filtering: Filter by title, author name, publication year (exact, range)
    - Searching: Full-text search on title and author name fields
    - Ordering: Sort by any book field with ascending/descending order
    
    Example Usage:
    - Filter: /api/books/?title=harry&author_name=rowling&publication_year_min=1990
    - Search: /api/books/?search=magic
    - Order: /api/books/?ordering=title,-publication_year
    
    Permissions: Read access for all users, write access for authenticated users only.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # =========================================================================
    # FILTER BACKENDS CONFIGURATION - ALL THREE FILTERS EXPLICITLY CONFIGURED
    # =========================================================================
    filter_backends = [
        rest_framework.DjangoFilterBackend,  # For Django Filter integration
        SearchFilter,                        # For search functionality
        OrderingFilter,                      # For ordering functionality
    ]
    
    # =========================================================================
    # DJANGO FILTER CONFIGURATION
    # =========================================================================
    filterset_class = BookFilter
    
    # =========================================================================
    # SEARCH FILTER CONFIGURATION
    # Search functionality on Book model fields: title and author
    # =========================================================================
    search_fields = [
        'title',           # Search in book titles (case-insensitive contains)
        'author__name',    # Search in author names (case-insensitive contains)
        '=title',          # Exact match search for title
        '=author__name',   # Exact match search for author name
    ]
    
    # =========================================================================
    # ORDERING FILTER CONFIGURATION
    # Allow users to order results by various fields
    # =========================================================================
    ordering_fields = [
        'title',              # Order by book title
        'publication_year',   # Order by publication year
        'author__name',       # Order by author name
        'id',                 # Order by primary key
    ]
    
    # Default ordering if no ordering parameter is provided
    ordering = ['title']
    
    def get_queryset(self):
        """
        Customize the queryset with additional filtering logic.
        This method can be extended for more complex filtering scenarios.
        """
        queryset = super().get_queryset()
        
        # Example of additional custom filtering
        min_year = self.request.query_params.get('min_year')
        max_year = self.request.query_params.get('max_year')
        
        if min_year:
            queryset = queryset.filter(publication_year__gte=min_year)
        if max_year:
            queryset = queryset.filter(publication_year__lte=max_year)
            
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        Override list method to include metadata about filtering, searching, and ordering options.
        """
        response = super().list(request, *args, **kwargs)
        
        # Add metadata about available filtering, searching, and ordering options
        response.data['metadata'] = {
            'filtering_options': {
                'title': 'Filter by title (contains)',
                'author_name': 'Filter by author name (contains)',
                'publication_year': 'Filter by exact publication year',
                'publication_year_min': 'Filter by minimum publication year',
                'publication_year_max': 'Filter by maximum publication year',
            },
            'searching_options': {
                'search': 'Full-text search in title and author name fields',
                'search_fields': self.search_fields,  # Explicitly show search fields
            },
            'ordering_options': {
                'ordering': f'Order by: {", ".join(self.ordering_fields)}',
                'default_ordering': self.ordering,
                'descending_order': 'Prefix field with "-" for descending order',
            },
            'example_queries': {
                'filter_by_author': '/api/books/?author_name=rowling',
                'search_books': '/api/books/?search=harry',
                'order_by_year': '/api/books/?ordering=-publication_year',
                'combined_query': '/api/books/?author_name=tolkien&ordering=title&publication_year_min=1950',
            }
        }
        
        return response


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    Maintains basic functionality while inheriting proper permissions.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'


class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Custom method called when creating a new book instance."""
        serializer.save()

    def create(self, request, *args, **kwargs):
        """Override create method to customize response."""
        response = super().create(request, *args, **kwargs)
        response.data['message'] = 'Book created successfully'
        response.data['status'] = 'success'
        return response


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        """Custom method called when updating a book instance."""
        serializer.save()

    def update(self, request, *args, **kwargs):
        """Override update method to customize response."""
        response = super().update(request, *args, **kwargs)
        response.data['message'] = 'Book updated successfully'
        response.data['status'] = 'success'
        return response


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        """Override destroy method to customize response."""
        instance = self.get_object()
        book_title = instance.title
        self.perform_destroy(instance)
        return Response({
            'message': f'Book "{book_title}" deleted successfully',
            'status': 'success'
        }, status=status.HTTP_200_OK)



class AuthorListView(generics.ListAPIView):
    """
    ListView for retrieving all authors with search and ordering capabilities.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Configure both SearchFilter and OrderingFilter
    filter_backends = [SearchFilter, OrderingFilter]
    
    # Search functionality on author name and book titles
    search_fields = [
        'name',           # Search in author names
        'books__title',   # Search in book titles of this author
    ]
    
    # Ordering configuration
    ordering_fields = [
        'name',    # Order by author name
        'id',      # Order by primary key
    ]
    ordering = ['name']  # Default ordering by name


class AuthorDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single author by ID with nested books.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'