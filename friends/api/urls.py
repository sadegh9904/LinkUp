from django.urls import path
from .views import SendFriendRequestView,SendedFriendRequestsView,ReceivedFriendRequestsView

urlpatterns = [
    path('send-request/', SendFriendRequestView.as_view(), name= 'sendrequest'),
    path('received-request/', ReceivedFriendRequestsView.as_view(), name= 'receivedrequest'),
    path('requests/', SendedFriendRequestsView.as_view(), name='requests'),
]
