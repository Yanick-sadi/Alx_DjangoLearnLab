from django.urls import path
from django.views.generic import TemplateView
from .views import (
    PostListView, PostDetailView, PostCreateView, 
    PostUpdateView, PostDeleteView, register, 
    CustomLoginView, CustomLogoutView, profile
)

urlpatterns = [
    # Blog Post CRUD URLs - Using the exact required patterns
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),  # Changed from 'posts/new/'
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),  # Changed from 'posts/<int:pk>/edit/'
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),  # Changed from 'posts/<int:pk>/delete/'
    
    # Authentication URLs
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
]