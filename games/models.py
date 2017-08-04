from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Room(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    #name = models.CharField(max_length=200)
    #firstPlayer = models.OneToOneField(User,related_name="firstPlayer",null=True)
    #secondPlayer = models.OneToOneField(User,related_name="secondPlayer",null=True)
    arePlaying = models.BooleanField(default=False)
    def __str__(self):
        return "Room " + str(self.id)

class Chat(models.Model):
    """
    for gomoku game
    """
    created = models.DateTimeField(auto_now_add=True)
    room = models.OneToOneField(Room)
    def __str__(self):
        return "chat " + str(self.id)
    
class Message(models.Model):
    """
    for gomoku game
    """
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    chat = models.ForeignKey(Chat)
    message = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username + " - " + self.message 


class GomokuGame(models.Model):

    room = models.ForeignKey(Room)
    board = models.TextField(default="{}")
    gameFinished = models.BooleanField(default=False)
    
    

class GomokuOnline(models.Model):

    user = models.OneToOneField(User)
    online = models.BooleanField(default=False)
    room = models.ForeignKey(Room, null=True)
    wantToPlay = models.BooleanField(default=False)
    readyToPlay = models.BooleanField(default=False)
    playing = models.BooleanField(default=False)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    currentGame = models.ForeignKey(GomokuGame,null=True)
    def __str__(self):
        return self.user.username




class BridgeRoom(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    turn = models.CharField(max_length=200,default="West")
    arePlaying = models.BooleanField(default=False)
    def __str__(self):
        return "BridgeRoom " + str(self.id)
  
  
class BridgeChat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    room = models.OneToOneField(BridgeRoom)
    def __str__(self):
        return "chat " + str(self.id)
      
class BridgeMessage(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    chat = models.ForeignKey(BridgeChat)
    message = models.CharField(max_length=200)
  
    def __str__(self):
        return self.user.username + " - " + self.message 
  
  
class BridgeGame(models.Model):
    room = models.ForeignKey(BridgeRoom)
    board = models.TextField(default="{}")
    gameFinished = models.BooleanField(default=False)
      
class BridgeOnline(models.Model):
    user = models.OneToOneField(User)
    online = models.BooleanField(default=False)
    room = models.ForeignKey(BridgeRoom,null=True)
    wantToPlay = models.BooleanField(default=False)
    readyToPlay = models.BooleanField(default=False)
    playing = models.BooleanField(default=False)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    currentGame = models.ForeignKey(BridgeGame,null=True)
    side = models.CharField(max_length=200,default="")
    def __str__(self):
        return self.user.username
     
 
     

    

    
