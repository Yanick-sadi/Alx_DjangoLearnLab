from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    PostUpdateView, 
    PostDeleteView
)

app_name = 'blog'

urlpatterns = [
    # Class-based views for CRUD operations
    path('', PostListView.as_view(), name='posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    
    # Authentication pages
    path('login/', TemplateView.as_view(template_name='blog/login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='blog/register.html'), name='register'),
]