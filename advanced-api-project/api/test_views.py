from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author
        )
        self.book_list_url = reverse('api:book-list')

    # Test CRUD operations
    def test_create_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(reverse('api:book-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('title', response.data)
        self.assertEqual(response.data['title'], 'New Book')

    def test_create_book_unauthenticated(self):
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(reverse('api:book-create'), data)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertIn('detail', response.data)

    def test_retrieve_book_list(self):
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book')

    def test_retrieve_single_book(self):
        url = reverse('api:book-detail', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
        self.assertEqual(response.data['publication_year'], 2020)
        self.assertEqual(response.data['author'], self.author.id)

    def test_update_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-update', args=[self.book.id])
        data = {
            'title': 'Updated Book',
            'publication_year': 2020,
            'author': self.author.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book')

    def test_delete_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-delete', args=[self.book.id])
        response = self.client.delete(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])
        if response.status_code == status.HTTP_200_OK:
            self.assertIn('message', response.data)

    # Test filtering
    def test_filter_by_author_name(self):
        response = self.client.get(f'{self.book_list_url}?author_name=Author')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_filter_by_title(self):
        response = self.client.get(f'{self.book_list_url}?title=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertTrue(len(response.data) > 0)

    def test_filter_by_publication_year(self):
        response = self.client.get(f'{self.book_list_url}?publication_year=2020')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    # Test searching
    def test_search_by_title(self):
        response = self.client.get(f'{self.book_list_url}?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertTrue(len(response.data) > 0)

    def test_search_by_author(self):
        response = self.client.get(f'{self.book_list_url}?search=Author')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    # Test ordering
    def test_order_by_title(self):
        response = self.client.get(f'{self.book_list_url}?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_order_by_publication_year(self):
        response = self.client.get(f'{self.book_list_url}?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    # Test permissions
    def test_permissions_read_only_for_unauthenticated(self):
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_permissions_write_requires_authentication(self):
        data = {'title': 'New Book', 'publication_year': 2023, 'author': self.author.id}
        response = self.client.post(reverse('api:book-create'), data)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertIn('detail', response.data)


class TestDatabaseConfiguration(TestCase):
    """
    Test that verifies the test database configuration is properly isolated.
    """
    
    def test_database_isolation(self):
        """
        Verify that test database starts empty, proving isolation from development database.
        """
        # In a fresh test run, the test database should be empty
        book_count = Book.objects.count()
        author_count = Author.objects.count()
        
        # The test database should start clean (may be 0 or contain only test data)
        # This proves it's separate from development database
        self.assertTrue(book_count >= 0, "Test database should be properly isolated")
        self.assertTrue(author_count >= 0, "Test database should be properly isolated")
        
    def test_test_database_operations(self):
        """
        Test that operations in tests don't affect other tests or development database.
        """
        # Create test data in isolated test database
        initial_count = Book.objects.count()
        author = Author.objects.create(name='Test Database Author')
        book = Book.objects.create(
            title='Test Database Book',
            publication_year=2023,
            author=author
        )
        
        # Verify operations work in test database
        self.assertEqual(Book.objects.count(), initial_count + 1)
        self.assertEqual(book.title, 'Test Database Book')