from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .models import Profile, Post, Comment, Tag

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image']

class PostForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas (e.g., django, python, web-development)'
        }),
        help_text="Separate tags with commas. Maximum 10 tags allowed."
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your blog post content here...',
                'rows': 15
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Pre-fill tags for existing posts
            self.fields['tags_input'].initial = ', '.join([tag.name for tag in self.instance.tags.all()])
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 50:
            raise forms.ValidationError("Content must be at least 50 characters long.")
        return content
    
    def clean_tags_input(self):
        tags_input = self.cleaned_data.get('tags_input')
        if tags_input:
            tag_names = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            if len(tag_names) > 10:
                raise forms.ValidationError("You can add maximum 10 tags.")
            # Check for excessively long tags
            for tag_name in tag_names:
                if len(tag_name) > 50:
                    raise forms.ValidationError(f"Tag '{tag_name}' is too long. Maximum 50 characters per tag.")
        return tags_input
    
    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            
            # Handle tags
            if self.cleaned_data['tags_input']:
                tag_names = [tag.strip() for tag in self.cleaned_data['tags_input'].split(',') if tag.strip()]
                tags = []
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name,
                        defaults={'slug': slugify(tag_name)}
                    )
                    tags.append(tag)
                post.tags.set(tags)
            else:
                post.tags.clear()
                
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here... (Minimum 10 characters, maximum 1000)',
                'rows': 4,
                'maxlength': '1000'
            }),
        }
        labels = {
            'content': 'Your Comment'
        }
        help_texts = {
            'content': 'Comments must be between 10 and 1000 characters.'
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        
        # Check if content is provided
        if not content:
            raise ValidationError("Comment content is required.")
        
        # Strip whitespace and check minimum length
        content_stripped = content.strip()
        if len(content_stripped) < 10:
            raise ValidationError("Comment must be at least 10 characters long (excluding whitespace).")
        
        # Check maximum length
        if len(content) > 1000:
            raise ValidationError("Comment cannot exceed 1000 characters.")
        
        # Check for meaningful content (not just repeated characters)
        if self._is_repeated_characters(content_stripped):
            raise ValidationError("Comment must contain meaningful content.")
        
        # Check for excessive whitespace
        if self._has_excessive_whitespace(content):
            raise ValidationError("Comment contains excessive whitespace.")
        
        return content
    
    def _is_repeated_characters(self, text):
        """Check if text consists of mostly repeated characters"""
        if len(text) < 3:
            return False
        # If more than 80% of characters are the same, consider it spam
        from collections import Counter
        char_counts = Counter(text)
        most_common_count = char_counts.most_common(1)[0][1]
        return most_common_count / len(text) > 0.8
    
    def _has_excessive_whitespace(self, text):
        """Check for excessive consecutive whitespace"""
        import re
        # Check for more than 3 consecutive spaces or newlines
        if re.search(r' {4,}', text):  # 4 or more spaces
            return True
        if re.search(r'\n{4,}', text):  # 4 or more newlines
            return True
        return False