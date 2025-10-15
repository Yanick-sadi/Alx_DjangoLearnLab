from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post

# List View - Display all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5

# Detail View - Display single post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# Create View - Create new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    success_url = '/blog/'  # Use absolute URL
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update View - Update existing post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return f'/blog/post/{self.object.pk}/'  # Redirect to post detail
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Delete View - Delete post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/blog/'  # Use absolute URL
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Keep function-based view for compatibility
def post_list(request):
    posts = Post.objects.all().order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})