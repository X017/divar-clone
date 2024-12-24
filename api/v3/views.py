from http.client import ResponseNotReady
from django.contrib.auth import login, logout
from django.core import paginator
from django.core.serializers import serialize
from django.db.models import query
from django.http import request
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
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
from .pagination import CustomPagination
from .tasks import start_otp
from accounts.models import CustomUser


class ListingHandler(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    lookup_field = 'uid'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = ListingFilters
    pagination_class = CustomPagination()
    http_method_names = ['get','post','patch','put','delete']
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        phone_number = user.phone_number  # Assuming user model has a phone_number field
        serializer.save(author=user, phone_number=phone_number)

    @action(detail=False, methods=['get'])   
    def user_profile(self, request):
        user = self.request.user
        listings = Listing.objects.filter(author=user, is_deleted=False)

        # Apply pagination
        paginator = CustomPagination()
        page = paginator.paginate_queryset(listings, request)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = paginator.get_paginated_response(serializer.data)
            user_data = {
                "username": user.username,
                "phone_number": user.phone_number,
                "created_at": user.created_at,
                "listings": paginated_response.data
            }
            return Response({"user_profile": user_data}, status=status.HTTP_200_OK)

        serializer = ListingSerializer(listings, many=True)
        user_data = {
            "username": user.username,
            "phone_number": user.phone_number,
            "created_at": user.created_at,
            "listings": serializer.data
        }
        return Response({"user_profile": user_data}, status=status.HTTP_200_OK)


    def destroy(self, request, uid=None):
        listing = get_object_or_404(Listing, uid=uid)
        listing.is_deleted = True
        listing.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class SignInAPI(APIView):
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
    

class CustomLoginAPI(APIView):
    def post(self,request,*args,**kwargs):
        username = request.data.get('username')
        phone_number = request.data.get('phone_number')
        queryset = CustomUser.objects.filter(username=username,phone_number=phone_number)
        
        
        if not queryset.exists():
            return Response({"detail":"username or password doesnt exists!"})
        else:
            start_otp.delay("")
            return Response({"detail":"Successully Started The Task!"})
        



