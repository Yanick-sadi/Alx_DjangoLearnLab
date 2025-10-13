import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from api.models import Book, Author

def check_database_state():
    print("🔍 Checking Database State")
    print("=" * 50)
    
    # Count objects in current database
    book_count = Book.objects.count()
    author_count = Author.objects.count()
    
    print(f"Development Database:")
    print(f"  - Books: {book_count}")
    print(f"  - Authors: {author_count}")
    
    print("\nWhen tests run, a separate test database will be created")
    print("with different object counts, proving isolation.")

if __name__ == "__main__":
    check_database_state()