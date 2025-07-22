from rest_framework import serializers
from friends.models import FriendRequest,Messages
from users .models import CustomUser


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'display_name', 'bio']
        
        

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserMiniSerializer(read_only = True)
    to_user = UserMiniSerializer(read_only= True)
    
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'is_active', 'timestamp']
        
        
        
class SendFriendRequestSerializer(serializers.ModelSerializer):
    to_user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    
    class Meta:
        model = FriendRequest
        fields = ['to_user']
        
    
    def validate_to_user(self, value):
        request = self.context['request']
        
        if value == request.user:
            raise serializers.ValidationError('Can not send request to yourself.')
        if FriendRequest.objects.filter(from_user = request.user, to_user=value, is_active = True).exists():
            raise serializers.ValidationError('Friend request already sent.')
        
        return value
    
    def create(self, validated_data):
        from_user = self.context['request'].user
        to_user = validated_data['to_user']
        return FriendRequest.objects.create(from_user=from_user, to_user=to_user)
    
    
    
class FriendListSerializer(serializers.ModelSerializer):
    friends = UserMiniSerializer(many=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'display_name', 'email', 'friends']
        
        
        
class MessagesSerializzer(serializers.ModelSerializer):
    
    class Meta:
        model = Messages
        fields = ['id', 'sender', 'receiver', 'text', 'timestamps']
        read_only_fields = ['sender', 'timestamps']