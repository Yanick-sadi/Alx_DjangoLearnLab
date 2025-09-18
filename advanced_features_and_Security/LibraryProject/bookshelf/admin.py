from django.contrib import admin

# Register your models here.
from .models import Book

class BookAdmin(admin.ModelAdmin):
    # Columns to show in the list view
    list_display = ("title", "author", "publication_year")

    # Add search bar for these fields
    search_fields = ("title", "author")

    # Add filter sidebar for publication_year
    list_filter = ("publication_year",)

# Register the model + custom admin
admin.site.register(Book, BookAdmin)
