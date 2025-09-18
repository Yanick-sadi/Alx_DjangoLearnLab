# bookshelf/forms.py
from django import forms
from .models import Book

# ✅ Example form for CSRF/security demonstration
class ExampleForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Your Name")
    email = forms.EmailField(required=True, label="Email Address")
    message = forms.CharField(
        widget=forms.Textarea,
        required=True,
        label="Message"
    )

# ✅ Model form for Book (safe input handling)
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]
