from django.urls import path
from django.views.generic import TemplateView
from .views import (
    PostListView, PostDetailView, PostCreateView, 
    PostUpdateView, PostDeleteView, register, 
    CustomLoginView, CustomLogoutView, profile,
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    posts_by_tag, search_posts, advanced_search,
    PostByTagListView  # Add this import
)

urlpatterns = [
    # Blog Post CRUD URLs
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    
    # Comment URLs
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    
    # Tag and Search URLs - Complete configuration with PostByTagListView
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts_by_tag'),  # Class-based view
    path('search/', search_posts, name='search_posts'),
    path('search/advanced/', advanced_search, name='advanced_search'),
    
    # Authentication URLs
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
]