from django import forms
from django_filters import FilterSet
from .models import Post, Author
import django_filters as filters
from django_filters import CharFilter


# создаём фильтр
class PostFilter(FilterSet):
    author = filters.ModelChoiceFilter(field_name='author', label='Автор', lookup_expr='exact',
                                       queryset=Author.objects.all())
    title = filters.CharFilter(label='Заголовок содержит', lookup_expr='icontains')
    dateCreation = filters.DateFilter(label='Дата создания позже, чем', lookup_expr='gt',
                                      widget=forms.DateInput(attrs=dict(placeholder='формат - DD.MM.YYYY')))

    class Meta:
        model = Post
        fields = ['author', 'title', 'dateCreation']
