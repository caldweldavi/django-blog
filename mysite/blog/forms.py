from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    """Form for sharing posts by email."""
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    """Form for adding comments to a post."""
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']