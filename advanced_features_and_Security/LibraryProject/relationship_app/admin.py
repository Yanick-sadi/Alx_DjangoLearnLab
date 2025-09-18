from django.contrib import admin
from .models import Library, Book, UserProfile

admin.site.register(Library)
admin.site.register(Book)
admin.site.register(UserProfile)
