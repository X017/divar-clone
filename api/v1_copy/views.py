from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas.coreapi import serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAuthorOrReadOnly
from listing.models import Listing

from .filters import ListingFilters
from .serializers import ListingSerializer, SignInSerializer

class ListingListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]    
    permission_classes = [IsAuthenticated]
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ListingFilters
    #permission_classes = [IsAuthenticatedOrReadOnly]
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request":self.request})
        return context
    

    def perform_create(self, serializer):
        user = self.request.user
        phone_number = user.phone_number
        # Ensure these fields are synced properly
        serializer.save(author=user, phone_number=phone_number)



class ListingView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    queryset = Listing.objects.filter(is_deleted=False)
    serializer_class = ListingSerializer


class SignUpAPI(APIView):
    permission_classes = [AllowAny]
    def post(self,request, *args, **kwargs):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user) # type: ignore[attr-defined]
            return Response({
                'refresh':str(refresh),
                'access':str(refresh.access_token)
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogOutAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        request.auth.delete()
        return Response({"detail":"Successully logged out!"})
    


class CurrentUserListings(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ListingSerializer
    def get_queryset(self):
        user = self.request.user
        return Listing.objects.filter(author=user,is_deleted=False)
    
class ListingDeleteView(generics.RetrieveDestroyAPIView):
        authentication_classes = [JWTAuthentication, IsAuthorOrReadOnly]
        permission_classes = [IsAuthenticated]
        serializer_class = ListingSerializer
        def delete(self, request, pk,*args, **kwargs):
            pk = pk
            listing = get_object_or_404(Listing,pk=pk)
            if listing.author == request.user:
                listing.is_deleted = True
                listing.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_403_FORBIDDEN)
