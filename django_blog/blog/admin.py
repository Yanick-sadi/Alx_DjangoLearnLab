from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, Profile, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date', 'get_comments_count']
    list_filter = ['published_date', 'author']
    search_fields = ['title', 'content']
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    get_comments_count.short_description = 'Comments'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at', 'active']
    list_filter = ['created_at', 'active', 'author']
    search_fields = ['content', 'author__username', 'post__title']
    list_editable = ['active']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']
    search_fields = ['user__username', 'bio']