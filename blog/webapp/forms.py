from django import forms
from django.forms import widgets

from webapp.models import Category, Article, Comment


class ArticleForm(forms.ModelForm):
    tags = forms.CharField(max_length=200, required=False, label='Тег')
    class Meta:
        model = Article
        fields = ['title', 'author', 'text', 'category']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['article', 'text', 'author']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")