from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.db import models
from .models import Post, Profile, Comment, Tag
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PostForm, CommentForm

# Authentication Views (keep existing)
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'blog/login.html'
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    template_name = 'blog/logout.html'

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'blog/profile.html', context)

# Blog Post CRUD Views with Enhanced Search and Tagging
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        tag_slug = self.request.GET.get('tag')
        author_name = self.request.GET.get('author')
        
        # Build complex query using Q objects
        query_filters = Q()
        
        if search_query:
            # Search in title, content, author username, and tags
            query_filters &= (
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(author__username__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            )
        
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            query_filters &= Q(tags__in=[tag])
        
        if author_name:
            query_filters &= Q(author__username__icontains=author_name)
        
        if query_filters:
            queryset = queryset.filter(query_filters).distinct()
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['tag_slug'] = self.request.GET.get('tag', '')
        context['author_name'] = self.request.GET.get('author', '')
        # Get popular tags (tags with most posts)
        context['popular_tags'] = Tag.objects.annotate(
            post_count=models.Count('posts')
        ).order_by('-post_count')[:10]
        return context

# New Class-Based View for Posts by Tag
class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5
    
    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        return Post.objects.filter(tags__in=[self.tag]).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['popular_tags'] = Tag.objects.annotate(
            post_count=models.Count('posts')
        ).order_by('-post_count')[:10]
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(active=True)
        context['comment_form'] = CommentForm()
        # Get related posts (posts with same tags)
        context['related_posts'] = Post.objects.filter(
            tags__in=list(self.object.tags.all())
        ).exclude(pk=self.object.pk).distinct()[:5]
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Comment Views
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_create.html'
    
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, 'Your comment has been added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Your comment has been updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Your comment has been deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

# Enhanced Tag and Search Views
def posts_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags__in=[tag]).order_by('-published_date')
    
    context = {
        'tag': tag,
        'posts': posts,
        'popular_tags': Tag.objects.annotate(post_count=models.Count('posts')).order_by('-post_count')[:10],
    }
    return render(request, 'blog/posts_by_tag.html', context)

def search_posts(request):
    query = request.GET.get('q', '')
    tag_filter = request.GET.get('tag', '')
    author_filter = request.GET.get('author', '')
    
    posts = Post.objects.all().order_by('-published_date')
    
    # Build complex query using Q objects
    query_filters = Q()
    
    if query:
        query_filters &= (
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(tags__name__icontains=query)
        )
    
    if tag_filter:
        tag = get_object_or_404(Tag, slug=tag_filter)
        query_filters &= Q(tags__in=[tag])
    
    if author_filter:
        query_filters &= Q(author__username__icontains=author_filter)
    
    if query_filters:
        posts = posts.filter(query_filters).distinct()
    
    context = {
        'posts': posts,
        'query': query,
        'tag_filter': tag_filter,
        'author_filter': author_filter,
        'results_count': posts.count(),
        'popular_tags': Tag.objects.annotate(post_count=models.Count('posts')).order_by('-post_count')[:10],
        'recent_authors': User.objects.filter(
            posts__isnull=False
        ).distinct().order_by('-date_joined')[:5],
    }
    return render(request, 'blog/search_results.html', context)

# Advanced search page
def advanced_search(request):
    popular_tags = Tag.objects.annotate(post_count=models.Count('posts')).order_by('-post_count')[:15]
    recent_authors = User.objects.filter(
        posts__isnull=False
    ).distinct().order_by('-date_joined')[:10]
    
    context = {
        'popular_tags': popular_tags,
        'recent_authors': recent_authors,
    }
    return render(request, 'blog/advanced_search.html', context)

# Function-based view for posts (for compatibility)
def post_list(request):
    posts = Post.objects.all().order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})