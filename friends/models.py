from django.db import models
from users.models import CustomUser

# Create your models here.
class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['from_user','to_user'], name='unique_friend_request')
        ]