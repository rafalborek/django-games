from django.test import TestCase
from django.contrib.auth.models import User
from .models import Chat, GomokuOnline, Message, Room, GomokuGame
from .models import BridgeChat, BridgeOnline, BridgeMessage, BridgeRoom, BridgeGame
from django.test import Client



class RoomCountTestCase(TestCase):
    """
    check if rooms are created and count them
    """
    def setUp(self):
        Room.objects.create()
        Room.objects.create()

    def test_room_count(self):
        self.assertEqual(Room.objects.all().count(),2)
        



class MessageChatTestCase(TestCase):
    """
    check if message is create correctly 
    """
    def setUp(self):
        room = Room.objects.create()
        user = User.objects.create_user("test", "test@test.test", "test")
        chat = Chat.objects.create(room=room)
        self.message = Message.objects.create(chat=chat,user=user,message="testuje")

    def test_message(self):
        self.assertEqual(self.message.message,"testuje")
        
class PageTestCase(TestCase):
    """
    check if server responds correctly
    """
    def setUp(self):
        user = User.objects.create_user("test", "test@test.test", "test")

    def test_response_200(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_redirect_if_not_login(self):
        client = Client()
        response = client.get('/gomoku/')
        self.assertRedirects(response, '/')
        response = client.get('/bridge/')
        self.assertRedirects(response, '/')
        
        
                
