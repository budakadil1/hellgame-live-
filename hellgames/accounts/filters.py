import django_filters
from django_filters import DateFilter, CharFilter, RangeFilter
from django import forms
from .models import *

class PostFilter(django_filters.FilterSet):
    title_search = CharFilter(field_name="post_title", label="Search:", lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control'}))
    start_date = DateFilter(field_name="date", label="From Date:", lookup_expr='gte', widget=forms.DateInput(attrs={'type':'date', 'class':'form-control'}))
    end_date = DateFilter(field_name="date", label="To Date:", lookup_expr='lte', widget=forms.DateInput(attrs={'type':'date', 'class':'form-control'}))
    price = RangeFilter(field_name="price",label="Price Range:",widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'Price', 'class':'form-control', 'color':'black'}))
    class Meta:
        model = gamePost
        fields = []

class GameFilter(django_filters.FilterSet):
    title_search = CharFilter(field_name="game_name", label="Search by title:", lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Search by title...'}))
    class Meta:
        model = gameIdentifier
        fields = []

   