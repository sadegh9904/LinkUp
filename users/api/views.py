from rest_framework import generics,status
from users.models import CustomUser
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import UserRegisterSerializer,EmailTokenObtainPairSerializer,UserProfileSerializer,ChangePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
    
        user = CustomUser.objects.get(email=request.data['email'])
        
        refresh = RefreshToken.for_user(user)
        
        response.data['refresh'] = str(refresh)
        response.data['access'] = str(refresh.access_token)
        
        return response
    
    

class LoginView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
    
    
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    
    
class ChangePasswordView(generics.RetrieveUpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = get_user_model()
    permission_classes = IsAuthenticated
    
    def get_queryset(self, queryset=None):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            
            if not self.object.check_password(old_password):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            
            self.object.set_password(new_password)
            self.object.save()
            
            
            return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    