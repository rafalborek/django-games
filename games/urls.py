from django.conf.urls import url, include
from . import views

app_name = 'games'

urlpatterns = [
    url(r'^gomoku/$', views.GomokuView.as_view(), name='gomoku'),
    url(r'^gomokuPlayers/$',views.PlayerInGame.as_view(), name='gomokuPlayers'),
    url(r'^gomokuRooms/$',views.GomokuRooms.as_view(), name='gomokuRooms'),
    url(r'^gomokuGame/$',views.GomokuGameView.as_view(), name='gomokuGame'),
    url(r'^gomokuStartGame/$',views.GomokuStartGameView.as_view(), name='gomokuStartGame'),
    url(r'^gomokuGameBoard/$',views.GomokuGameBoardView.as_view(), name='gomokuBoardGame'),
    url(r'^gomokuGame/(?P<room_id>[0-9]+)/$',views.GomokuJoinGameView.as_view(), name="gomokuJoinGame"),
    url(r'^addMessagesToChat/$', views.AddMessagesToChatView.as_view(), name='addMessagesToChat'),
    url(r'^getMessagesFromChat/$', views.SendMessagesToUser.as_view(), name='sendMessagesToUser'),
    url(r'^bridge/$', views.BridgeView.as_view(), name='bridge'),
    url(r'^bridgeGame/$',views.BridgeGameView.as_view(), name='bridgeGame'),
    url(r'^bridgeStartGame/$',views.BridgeStartGameView.as_view(), name='bridgeStartGame'),
    url(r'^bridgeGameBoard/$',views.BridgeGameBoardView.as_view(), name='bridgeBoardGame'),
    url(r'^bridgeGame/(?P<room_id>[0-9]+)/$',views.BridgeJoinGameView.as_view(), name="bridgeJoinGame"),
    url(r'^addMessagesToChatBridge/$', views.AddMessagesToChatViewBridge.as_view(), name='addMessagesToChatBridge'),
    url(r'^getMessagesFromChatBridge/$', views.SendMessagesToUserBridge.as_view(), name='sendMessagesToUserBridge'),
    
]
