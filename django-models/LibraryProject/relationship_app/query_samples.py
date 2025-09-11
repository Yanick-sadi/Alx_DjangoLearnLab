# query_samples.py
# Demonstrates queries on ForeignKey, ManyToMany, and OneToOne relationships.

import os
import django

# 1. Point Django to your project settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

# 2. Setup Django
django.setup()

# 3. Now safely import your models
from relationship_app.models import Author, Book, Library, Librarian

# --------------------------
# ForeignKey: One Author -> Many Books
# --------------------------
# Create author and books (if not already created)
author_name = "George Orwell"
author, created = Author.objects.get_or_create(name=author_name)
book1, _ = Book.objects.get_or_create(title="1984", author=author)
book2, _ = Book.objects.get_or_create(title="Animal Farm", author=author)

# Retrieve author from database using .get()
author = Author.objects.get(name=author_name)

books_by_orwell = Book.objects.filter(author=author)
print("Books by George Orwell:")
for book in books_by_orwell:
    print(f"- {book.title}")

# --------------------------
# ManyToMany: Library -> Books
# --------------------------
library_name = "Central Library"
library, created = Library.objects.get_or_create(name=library_name)
library.books.add(book1, book2)  # ensure books are added

# Retrieve library from database using .get()
library = Library.objects.get(name=library_name)

print(f"\nBooks in {library.name}:")
for book in library.books.all():
    print(f"- {book.title}")

# --------------------------
# OneToOne: Librarian -> Library
# --------------------------
librarian_name = "Alice"
librarian, created = Librarian.objects.get_or_create(name=librarian_name, library=library)

# Retrieve librarian via library
librarian = Librarian.objects.get(library=library)

print(f"\nLibrarian of {library.name}: {librarian.name}")
