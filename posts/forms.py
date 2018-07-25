from django import forms
# from django.shortcuts import request

from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

class EditPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('text', )

    
