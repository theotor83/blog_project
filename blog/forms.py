from django import forms
from . import models

class PostForm(forms.ModelForm):
    class Meta:
        model = models.BlogPost
        fields = ['title','text','image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...',
                'style': 'resize: none;'
            }),
        }