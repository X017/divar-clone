import django_filters as filters
from listing.models import Listing


class ListingFilters(filters.FilterSet):
    title = filters.CharFilter(field_name="title",lookup_expr='icontains')
    price = filters.NumberFilter()
    price__gt = filters.NumberFilter(field_name='price',lookup_expr='gt')
    price__lt = filters.NumberFilter(field_name='price',lookup_expr='lt')

    



    class Meta:
        model = Listing
        fields = ['title','price']