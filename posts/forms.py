from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea)

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image'
        ]