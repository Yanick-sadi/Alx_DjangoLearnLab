from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
    
    def get_comments_count(self):
        return self.comments.count()
    
    class Meta:
        ordering = ['-published_date']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.post.pk})
    
    class Meta:
        ordering = ['created_at']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'