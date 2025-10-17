from django.contrib import admin
from .models import Post, Profile, Comment, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date', 'get_comments_count', 'get_tags']
    list_filter = ['published_date', 'author', 'tags']
    search_fields = ['title', 'content', 'tags__name']
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    get_comments_count.short_description = 'Comments'
    
    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_post_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def get_post_count(self, obj):
        return obj.posts.count()
    get_post_count.short_description = 'Posts'

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