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
author = Author.objects.create(name="George Orwell")
book1 = Book.objects.create(title="1984", author=author)
book2 = Book.objects.create(title="Animal Farm", author=author)

books_by_orwell = Book.objects.filter(author=author)
print("Books by George Orwell:")
for book in books_by_orwell:
    print(f"- {book.title}")

# --------------------------
# ManyToMany: Library -> Books
# --------------------------
library = Library.objects.create(name="Central Library")
library.books.add(book1, book2)

print(f"\nBooks in {library.name}:")
for book in library.books.all():
    print(f"- {book.title}")

library_name = "Central Library"
library = Library.objects.get(name=library_name)
# --------------------------
# OneToOne: Librarian -> Library
# --------------------------
librarian = Librarian.objects.create(name="Alice", library=library)

print(f"\nLibrarian of {library.name}: {librarian.name}")
