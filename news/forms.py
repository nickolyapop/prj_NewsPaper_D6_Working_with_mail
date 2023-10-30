from django.forms import ModelForm

from .models import Post
from django import forms

# Создаём модельную форму
class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['author', 'title', 'category', 'text']
        widgets = {
            'author': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя автора',
          }),
          'title' : forms.TextInput(attrs={
            'class': 'form-control',
          }),
          'category' : forms.SelectMultiple (attrs={
            'class': 'form-control',
          }),
          'text' : forms.Textarea(attrs={
            'class': 'form-control',
          }),
        }
        labels = {
            'author': 'Автор',
            'title': 'Заголовок',
            'category': 'Категория',
            'text': 'Текст',
        }
