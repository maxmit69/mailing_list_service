from django import forms
from blogs_app.models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content', 'image',)