from django import forms
from .models import Post




class PostForm2(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'attachment']  # Include attachment field
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'What\'s on your mind?', 'rows': 4, 'cols': 40})
        }