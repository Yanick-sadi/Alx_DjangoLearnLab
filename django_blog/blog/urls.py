from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='posts'),
    path('login/', TemplateView.as_view(template_name='blog/login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='blog/register.html'), name='register'),
]