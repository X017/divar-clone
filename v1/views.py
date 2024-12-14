from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ListingSerializer
from .filters import ListingFilters
from listing.models import Listing
from rest_framework.viewsets import ModelViewSet



class ListingListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ListingFilters
    #permission_classes = [IsAuthenticatedOrReadOnly]

class ListingView(generics.ListAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


