
from django_filters import rest_framework as filters
from django_filters import CharFilter

from .models import Quote


class SearchFilter(filters.FilterSet):
    body = CharFilter(field_name='body', lookup_expr="icontains")
    class Meta:
        model = Quote
        fields = ('body',)
