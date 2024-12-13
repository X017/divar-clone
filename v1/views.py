from rest_framework import generics
from listing.models import Listing
from .serializers import ListingSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .filters import ListingFilters
from django_filters.rest_framework import DjangoFilterBackend

class ListingListCreateView(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ListingFilters
    permission_classes = [IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user, contact=user)
