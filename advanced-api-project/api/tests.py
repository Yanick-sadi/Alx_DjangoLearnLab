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

    def test_create_book_unauthenticated(self):
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(reverse('api:book-create'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_book_list(self):
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_single_book(self):
        url = reverse('api:book-detail', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')

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

    def test_delete_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-delete', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test filtering
    def test_filter_by_author_name(self):
        response = self.client.get(f'{self.book_list_url}?author_name=Author')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_title(self):
        response = self.client.get(f'{self.book_list_url}?title=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_publication_year(self):
        response = self.client.get(f'{self.book_list_url}?publication_year=2020')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test searching
    def test_search_by_title(self):
        response = self.client.get(f'{self.book_list_url}?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_by_author(self):
        response = self.client.get(f'{self.book_list_url}?search=Author')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test ordering
    def test_order_by_title(self):
        response = self.client.get(f'{self.book_list_url}?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_by_publication_year(self):
        response = self.client.get(f'{self.book_list_url}?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test permissions
    def test_permissions_read_only_for_unauthenticated(self):
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permissions_write_requires_authentication(self):
        data = {'title': 'New Book', 'publication_year': 2023, 'author': self.author.id}
        response = self.client.post(reverse('api:book-create'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)