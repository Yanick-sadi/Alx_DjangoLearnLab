# bookshelf/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.csrf import csrf_protect
from .models import Book
from .forms import BookForm
from .forms import ExampleForm

# ✅ Book list view with permission check
@login_required
@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})

# ✅ Example form view (CSRF protected)
@csrf_protect
def example_form_view(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Secure handling of user input (no SQL injection risk with Django ORM)
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            # For now, just pass data back to template
            return render(request, "bookshelf/form_example.html", {
                "form": form,
                "submitted": True,
                "name": name,
                "email": email,
                "message": message
            })
    else:
        form = ExampleForm()

    return render(request, "bookshelf/form_example.html", {"form": form})
