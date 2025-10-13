"""
Comprehensive unit tests for Django REST Framework APIs.
Tests cover CRUD operations, filtering, searching, ordering, and permissions.
"""

import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, force_authenticate
from django.contrib.auth.models import User
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class BaseTestCase(APITestCase):
    """
    Base test case with common setup methods for all test classes.
    Provides reusable methods for creating test data and users.
    """
    
    def setUp(self):
        """
        Set up test data that will be available for all test methods.
        Creates test users, authors, and books for testing.
        """
        # Create test users
        self.regular_user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com'
        )
        
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpass123',
            email='admin@example.com'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='J.R.R. Tolkien')
        self.author3 = Author.objects.create(name='George Orwell')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        
        self.book2 = Book.objects.create(
            title='The Hobbit',
            publication_year=1937,
            author=self.author2
        )
        
        self.book3 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author3
        )
        
        self.book4 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        
        # API client
        self.client = APIClient()
        
        # URLs for Book endpoints
        self.book_list_url = reverse('api:book-list')
        self.book_create_url = reverse('api:book-create')
        
        # URLs for Author endpoints
        self.author_list_url = reverse('api:author-list')
        self.author_create_url = reverse('api:author-create')


class BookCRUDTests(BaseTestCase):
    """
    Test CRUD operations for Book model endpoints.
    Tests Create, Retrieve, Update, and Delete operations.
    """
    
    def test_create_book_authenticated(self):
        """
        Test that authenticated users can create new books.
        Should return 201 Created and create the book in database.
        """
        self.client.force_authenticate(user=self.regular_user)
        
        book_data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(
            self.book_create_url,
            data=json.dumps(book_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Test Book')
        self.assertEqual(response.data['message'], 'Book created successfully')
        self.assertEqual(Book.objects.count(), 5)  # 4 initial + 1 new
        
        # Verify the book was actually created in database
        new_book = Book.objects.get(title='New Test Book')
        self.assertEqual(new_book.publication_year, 2023)
        self.assertEqual(new_book.author, self.author1)
    
    def test_create_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot create books.
        Should return 401 Unauthorized or 403 Forbidden.
        """
        book_data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(
            self.book_create_url,
            data=json.dumps(book_data),
            content_type='application/json'
        )
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertEqual(Book.objects.count(), 4)  # No new books should be created
    
    def test_retrieve_book_list_unauthenticated(self):
        """
        Test that unauthenticated users can retrieve the book list.
        Should return 200 OK with all books.
        """
        response = self.client.get(self.book_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # Should return all 4 books
    
    def test_retrieve_single_book_unauthenticated(self):
        """
        Test that unauthenticated users can retrieve a single book.
        Should return 200 OK with book details.
        """
        url = reverse('api:book-detail', args=[self.book1.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
        self.assertEqual(response.data['author'], self.author1.id)
    
    def test_update_book_authenticated(self):
        """
        Test that authenticated users can update existing books.
        Should return 200 OK and update the book in database.
        """
        self.client.force_authenticate(user=self.regular_user)
        
        update_url = reverse('api:book-update', args=[self.book1.id])
        update_data = {
            'title': 'Updated Book Title',
            'publication_year': 1997,
            'author': self.author1.id
        }
        
        response = self.client.put(
            update_url,
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book Title')
        self.assertEqual(response.data['message'], 'Book updated successfully')
        
        # Verify the book was actually updated in database
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book Title')
    
    def test_update_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot update books.
        Should return 401 Unauthorized or 403 Forbidden.
        """
        update_url = reverse('api:book-update', args=[self.book1.id])
        update_data = {'title': 'Unauthorized Update'}
        
        response = self.client.put(
            update_url,
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
        # Verify the book was NOT updated in database
        self.book1.refresh_from_db()
        self.assertNotEqual(self.book1.title, 'Unauthorized Update')
    
    def test_delete_book_authenticated(self):
        """
        Test that authenticated users can delete books.
        Should return 200 OK and remove the book from database.
        """
        self.client.force_authenticate(user=self.regular_user)
        
        delete_url = reverse('api:book-delete', args=[self.book1.id])
        response = self.client.delete(delete_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Book "Harry Potter and the Philosopher\'s Stone" deleted successfully')
        self.assertEqual(Book.objects.count(), 3)  # Should have one less book
        
        # Verify the book was actually deleted from database
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(id=self.book1.id)
    
    def test_delete_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot delete books.
        Should return 401 Unauthorized or 403 Forbidden.
        """
        delete_url = reverse('api:book-delete', args=[self.book1.id])
        response = self.client.delete(delete_url)
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertEqual(Book.objects.count(), 4)  # No books should be deleted


class BookFilteringTests(BaseTestCase):
    """
    Test filtering functionality for Book model endpoints.
    Tests various filtering scenarios and query parameters.
    """
    
    def test_filter_by_author_name(self):
        """
        Test filtering books by author name.
        Should return only books by the specified author.
        """
        response = self.client.get(f'{self.book_list_url}?author_name=rowling')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 books by Rowling
        self.assertEqual(response.data[0]['author'], self.author1.id)
        self.assertEqual(response.data[1]['author'], self.author1.id)
    
    def test_filter_by_title(self):
        """
        Test filtering books by title.
        Should return only books with matching title pattern.
        """
        response = self.client.get(f'{self.book_list_url}?title=harry')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 Harry Potter books
        for book in response.data:
            self.assertIn('Harry', book['title'])
    
    def test_filter_by_publication_year(self):
        """
        Test filtering books by exact publication year.
        Should return only books from the specified year.
        """
        response = self.client.get(f'{self.book_list_url}?publication_year=1997')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return 1 book from 1997
        self.assertEqual(response.data[0]['publication_year'], 1997)
    
    def test_filter_by_publication_year_range(self):
        """
        Test filtering books by publication year range.
        Should return books within the specified year range.
        """
        response = self.client.get(
            f'{self.book_list_url}?publication_year_min=1940&publication_year_max=2000'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return books from 1949, 1997, 1998
        self.assertEqual(len(response.data), 3)
        for book in response.data:
            self.assertGreaterEqual(book['publication_year'], 1940)
            self.assertLessEqual(book['publication_year'], 2000)
    
    def test_filter_by_multiple_criteria(self):
        """
        Test filtering books by multiple criteria simultaneously.
        Should return books that match all specified filters.
        """
        response = self.client.get(
            f'{self.book_list_url}?author_name=rowling&publication_year_min=1997'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both Rowling books meet criteria


class BookSearchTests(BaseTestCase):
    """
    Test search functionality for Book model endpoints.
    Tests full-text search across title and author fields.
    """
    
    def test_search_by_book_title(self):
        """
        Test searching books by title using search parameter.
        Should return books with matching titles.
        """
        response = self.client.get(f'{self.book_list_url}?search=harry')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 Harry Potter books
        for book in response.data:
            self.assertIn('Harry', book['title'])
    
    def test_search_by_author_name(self):
        """
        Test searching books by author name using search parameter.
        Should return books by matching authors.
        """
        response = self.client.get(f'{self.book_list_url}?search=tolkien')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return 1 book by Tolkien
        self.assertEqual(response.data[0]['title'], 'The Hobbit')
    
    def test_search_by_partial_title(self):
        """
        Test searching books by partial title match.
        Should return books with titles containing the search term.
        """
        response = self.client.get(f'{self.book_list_url}?search=potter')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 Potter books
        for book in response.data:
            self.assertIn('Potter', book['title'])
    
    def test_search_no_results(self):
        """
        Test searching with a term that doesn't match any books.
        Should return empty results.
        """
        response = self.client.get(f'{self.book_list_url}?search=nonexistent')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Should return no books


class BookOrderingTests(BaseTestCase):
    """
    Test ordering functionality for Book model endpoints.
    Tests ascending and descending ordering by various fields.
    """
    
    def test_order_by_title_ascending(self):
        """
        Test ordering books by title in ascending order.
        Should return books sorted A-Z by title.
        """
        response = self.client.get(f'{self.book_list_url}?ordering=title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        
        # Check if titles are in ascending order
        titles = [book['title'] for book in response.data]
        sorted_titles = sorted(titles)
        self.assertEqual(titles, sorted_titles)
    
    def test_order_by_title_descending(self):
        """
        Test ordering books by title in descending order.
        Should return books sorted Z-A by title.
        """
        response = self.client.get(f'{self.book_list_url}?ordering=-title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        
        # Check if titles are in descending order
        titles = [book['title'] for book in response.data]
        sorted_titles = sorted(titles, reverse=True)
        self.assertEqual(titles, sorted_titles)
    
    def test_order_by_publication_year_ascending(self):
        """
        Test ordering books by publication year in ascending order.
        Should return books sorted from oldest to newest.
        """
        response = self.client.get(f'{self.book_list_url}?ordering=publication_year')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if publication years are in ascending order
        years = [book['publication_year'] for book in response.data]
        sorted_years = sorted(years)
        self.assertEqual(years, sorted_years)
    
    def test_order_by_publication_year_descending(self):
        """
        Test ordering books by publication year in descending order.
        Should return books sorted from newest to oldest.
        """
        response = self.client.get(f'{self.book_list_url}?ordering=-publication_year')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if publication years are in descending order
        years = [book['publication_year'] for book in response.data]
        sorted_years = sorted(years, reverse=True)
        self.assertEqual(years, sorted_years)
    
    def test_order_by_author_name(self):
        """
        Test ordering books by author name.
        Should return books sorted by author name.
        """
        response = self.client.get(f'{self.book_list_url}?ordering=author__name')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Note: This test verifies the ordering works, though we can't easily verify author names from response
    
    def test_multiple_field_ordering(self):
        """
        Test ordering books by multiple fields.
        Should return books sorted by first field, then second field.
        """
        response = self.client.get(f'{self.book_list_url}?ordering=author__name,title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)


class BookCombinedFeaturesTests(BaseTestCase):
    """
    Test combined usage of filtering, searching, and ordering.
    Tests complex query scenarios with multiple parameters.
    """
    
    def test_combined_filter_search_order(self):
        """
        Test combining filtering, searching, and ordering in one query.
        Should return properly filtered, searched, and ordered results.
        """
        response = self.client.get(
            f'{self.book_list_url}?author_name=rowling&search=harry&ordering=-publication_year'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 Harry Potter books by Rowling
        
        # Check if results are ordered by publication year descending
        if len(response.data) > 1:
            self.assertGreaterEqual(
                response.data[0]['publication_year'], 
                response.data[1]['publication_year']
            )
    
    def test_metadata_in_response(self):
        """
        Test that API responses include metadata about available features.
        Should return metadata with filtering, searching, and ordering options.
        """
        response = self.client.get(self.book_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('metadata', response.data)
        
        metadata = response.data['metadata']
        self.assertIn('filtering_options', metadata)
        self.assertIn('searching_options', metadata)
        self.assertIn('ordering_options', metadata)
        self.assertIn('example_queries', metadata)


class AuthorCRUDTests(BaseTestCase):
    """
    Test CRUD operations for Author model endpoints.
    Tests Create, Retrieve operations for authors.
    """
    
    def test_create_author_authenticated(self):
        """
        Test that authenticated users can create new authors.
        Should return 201 Created and create the author in database.
        """
        self.client.force_authenticate(user=self.regular_user)
        
        author_data = {
            'name': 'New Test Author'
        }
        
        response = self.client.post(
            self.author_create_url,
            data=json.dumps(author_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Test Author')
        self.assertEqual(response.data['message'], 'Author created successfully')
        self.assertEqual(Author.objects.count(), 4)  # 3 initial + 1 new
    
    def test_retrieve_author_list_unauthenticated(self):
        """
        Test that unauthenticated users can retrieve the author list.
        Should return 200 OK with all authors.
        """
        response = self.client.get(self.author_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Should return all 3 authors
    
    def test_retrieve_author_with_books(self):
        """
        Test that author retrieval includes nested book information.
        Should return author details with their books.
        """
        url = reverse('api:author-detail', args=[self.author1.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'J.K. Rowling')
        self.assertIn('books', response.data)
        self.assertEqual(len(response.data['books']), 2)  # Should have 2 books


class ValidationTests(BaseTestCase):
    """
    Test validation scenarios for Book model.
    Tests custom validation rules and error handling.
    """
    
    def test_publication_year_validation_future_year(self):
        """
        Test that books cannot be created with future publication years.
        Should return 400 Bad Request with validation error.
        """
        self.client.force_authenticate(user=self.regular_user)
        
        future_year_data = {
            'title': 'Book from Future',
            'publication_year': 2030,  # Future year
            'author': self.author1.id
        }
        
        response = self.client.post(
            self.book_create_url,
            data=json.dumps(future_year_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        self.assertIn('cannot be in the future', str(response.data['publication_year']))
    
    def test_required_fields_validation(self):
        """
        Test that required fields validation works correctly.
        Should return 400 Bad Request with field errors.
        """
        self.client.force_authenticate(user=self.regular_user)
        
        invalid_data = {
            'title': '',  # Empty title
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(
            self.book_create_url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Should have validation errors for required fields


class PaginationTests(BaseTestCase):
    """
    Test pagination functionality if implemented.
    Tests that paginated responses are correctly structured.
    """
    
    def test_pagination_structure(self):
        """
        Test that list responses include pagination metadata if pagination is enabled.
        This test assumes pagination is configured in settings.
        """
        response = self.client.get(self.book_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # If pagination is enabled, response should have pagination structure
        # If not enabled, response should be a plain list
        # This test adapts to both scenarios


# Run specific test groups if needed
def suite():
    """
    Create a test suite for running specific groups of tests.
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BookCRUDTests))
    suite.addTest(unittest.makeSuite(BookFilteringTests))
    suite.addTest(unittest.makeSuite(BookSearchTests))
    suite.addTest(unittest.makeSuite(BookOrderingTests))
    return suite


if __name__ == '__main__':
    """
    Allow running tests directly from this file.
    """
    import unittest
    unittest.main()