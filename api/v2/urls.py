from django.urls import path, include
from .views import  SignUpAPI , ListingHandler
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'listings',ListingHandler)

urlpatterns = [
    path('token/',TokenObtainPairView.as_view(),name='token-obtain-pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('sign-up/',SignUpAPI.as_view(),name='sing-up'),
    path('login/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('',include(router.urls))
]