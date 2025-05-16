from .views import UserRegisterView,LoginView,UserProfileView,ChangePasswordView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.urls import path


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name ='register'),
    path('login/', LoginView.as_view(), name ='login'),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('profile/', UserProfileView.as_view(), name ='profile'),
    path('change-password/', ChangePasswordView.as_view(), name ='change-password'),
]
