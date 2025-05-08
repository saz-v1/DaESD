from django import forms
from .models import Community, Post, Comment

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'visibility', 'attachment']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'visibility': forms.RadioSelect(attrs={'class': 'visibility-options'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'content': 'Comment',
        } 