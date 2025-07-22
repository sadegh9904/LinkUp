from rest_framework import generics,status
from friends.api import serializers
from friends.models import FriendRequest
from serializers import FriendRequestSerializer,SendFriendRequestSerializer,FriendListSerializer,UserMiniSerializer,MessagesSerializzer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied



class SendFriendRequestView(generics.CreateAPIView):
    serializer_class = SendFriendRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        return {'request' : self.request}
    
    
    
class ReceivedFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return FriendRequest.objects.filter(to_user= self.request.user, is_active=True)
    
    
    
class SendedFriendRequestsView(generics.ListAPIView):
    serializer_class = SendFriendRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return FriendRequest.objects.filter(from_user = self.request.user, is_active = True)
    
    
#for accept friends we must add both user to friends list    
class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        try:
            friend_request = FriendRequest.objects.get(pk=pk, to_user = request.user, is_active = True)
        except FriendRequest.DoesNotExist:
            return Response({"Error": "Friend request not found."}, status= status.HTTP_404_NOT_FOUND)
        
        from_user = friend_request.from_user
        to_user = friend_request.to_user
        
        from_user.friends.add(to_user)
        to_user.friends.add(from_user)
        
        friend_request.is_active = False
        friend_request.save()
        
        return Response({"detail":"Friend request accepted."}, status= status.HTTP_200_OK)
    
    

class RejectFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        try:
            friend_request = FriendRequest.objects.get(pk=pk, to_user=request.user, is_active = True)
        except FriendRequest.DoesNotExist:
            return Response({"Error": "Friend request not found."}, status= status.HTTP_404_NOT_FOUND)
        
        
        friend_request.is_active = False
        friend_request.save()
        
        return Response({"detail": "Friend request rejected."}, status= status.HTTP_200_OK)
    

class FriendsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserMiniSerializer
    
    def get_queryset(self):
        return self.request.user.friends.all()
    
    
    
class MessagesCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessagesSerializzer
    
    def perform_create(self, serializer):
        sender = self.request.user
        receiver = serializer.validated_data['receiver']
        
        if receiver not in sender.friends.all():
           raise PermissionDenied("You can only message your friends.") 
        serializer.save(sender = sender)
        
        

class MessagesListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessagesSerializzer
    
    
        sender = self.request.user
        receiver = serializer.validated_data['receiver']
    def get_queryset(self):
        
        return 
    