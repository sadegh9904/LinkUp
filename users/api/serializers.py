from users.models import CustomUser
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'display_name', 'bio']
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            display_name = validated_data.get('display_name', ''),
            bio = validated_data.get('bio', ''),
        )
        return user
    
    
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'display_name', 'bio']
        
        

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    

    
""" class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_lenth=8) """