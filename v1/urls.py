from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from .views import ListingListCreateView , ListingView, SignUpAPI
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('add/', ListingListCreateView.as_view(), name='listing-list-create'),
    path('token/',TokenObtainPairView.as_view(),name='token-obtain-pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('',ListingView.as_view(),name='main-page'),
    path('sign-up/',SignUpAPI.as_view(),name='sing-up'),
    path('login/',TokenObtainPairView.as_view(),name='token_obtain_pair')
]
