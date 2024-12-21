from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.schemas.coreapi import serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAuthorOrReadOnly
from listing.models import Listing

from .filters import ListingFilters
from .serializers import ListingSerializer, SignInSerializer


class ListingHandler(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    lookup_field = 'uid'
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticatedOrReadOnly,IsAuthenticatedOrReadOnly]
    filterset_classes = ListingFilters
    def perform_create(self, serializer):
        user = self.request.user
        phone_number = self.request.user 
        serializer.save(author=user, phone_number=phone_number)




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
    


