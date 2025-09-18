# bookshelf/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book

# List all books (requires login)
@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})


# View details of a single book
@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "bookshelf/book_detail.html", {"book": book})


# Add a new book (requires add permission)
@permission_required("bookshelf.add_book", raise_exception=True)
def book_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        description = request.POST.get("description")
        Book.objects.create(title=title, author=author, description=description)
        return redirect("book_list")
    return render(request, "bookshelf/book_form.html")


# Edit a book (requires change permission)
@permission_required("bookshelf.change_book", raise_exception=True)
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.description = request.POST.get("description")
        book.save()
        return redirect("book_list")
    return render(request, "bookshelf/book_form.html", {"book": book})


# Delete a book (requires delete permission)
@permission_required("bookshelf.delete_book", raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "bookshelf/book_confirm_delete.html", {"book": book})
