from rest_framework import generics
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet


from .serializers import ListingSerializer, SignInSerializer
from .filters import ListingFilters
from listing.models import Listing
from accounts.models import CustomUser
from .permissions import IsAuthorEnabled
from django.contrib.auth import login, logout

class ListingListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]    
    permission_classes = [IsAuthenticated, IsAuthorEnabled]
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
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer    


class SignUpAPI(APIView):
    permission_classes = [AllowAny]
    def post(self,request, *args, **kwargs):
        serializer = SignInSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
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
        return Listing.objects.filter(author=user)
         