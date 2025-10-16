from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Profile, Post, Comment

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