import django_filters as filters
from listing.models import Listing


class ListingFilters(filters.FilterSet):
    title = filters.CharFilter(field_name="title",lookup_expr='icontains')
    class Meta:
        model = Listing
        fields = {
            'title': ['icontains'],
            'price':['lt','gt'],
        }