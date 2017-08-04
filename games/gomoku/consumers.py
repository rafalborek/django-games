from channels import Channel, Group
from channels.sessions import channel_session, enforce_ordering
from channels.asgi import get_channel_layer
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
from django.contrib.auth.models import User
from games.models import Chat, GomokuOnline, Message, Room, GomokuGame
import json
from games.gomoku.functions import *
from games.gomoku.gomoku import *

@channel_session_user_from_http
def gomoku_ws_connect(message):
    if not message.user.is_authenticated():
        return
    
    channel_layer = get_channel_layer()
    ch_group_list = channel_layer.group_channels('gomoku')
    u = GomokuOnline.objects.get(user=message.user)
    u.online=True
    u.save()
    Group("gomoku").add(message.reply_channel)
    Group("gomoku-user-%s" % str(u.id)).add(message.reply_channel)
    playersOnlineHtml = playersOnline(message)
    gomokuRoomsHtml = gomokuRooms(message)
    data = {"playersOnlineHtml": playersOnlineHtml,
            "gomokuRoomsHtml" : gomokuRoomsHtml }
    
    Group("gomoku").send({
    "text" : json.dumps(data)
    })
    

@channel_session_user
def gomoku_ws_receive(message):
    if not message.user.is_authenticated():
        return
    data = {}
    if not to_json(data,message['text']):
        return
    
    u = GomokuOnline.objects.get(user=message.user)
    room = u.room
    
    
    if "inRoom" in data and room != None:
            Group("gomoku-room-%s" % str(room.id)).add(message.reply_channel)
            gomokuRoomsHtml = gomokuRooms(message)
            toSend = {"gomokuRoomsHtml" : gomokuRoomsHtml }
            Group("gomoku").send({
                "text" : json.dumps(toSend)
            })
            if room.arePlaying:
                player = GomokuOnline.objects.get(room=room,playing=True)[0]
                game = player.currentGame
                Group("gomoku-room-%s" % str(room.id)).send({
                    "text" : game.board
                })
            return 
    
    if "move" in data and u.playing:

        players = GomokuOnline.objects.filter(room=room,playing=True)
        game = u.currentGame
        board = json.loads(game.board)
        i = data["move"]["i"]
        j = data["move"]["j"]
        playerChar='x'
        if u == players[0]:
            playerChar = 'x'
        else:
            playerChar = 'o'
        if not Gomoku.makeMove(board["board"],i,j,playerChar):
            return
        dataToSend = {}
        dataToSend["myTurn"] = False 
        game.board = json.dumps(board)
        game.save()
        
        Group("gomoku-room-%s" % str(room.id)).send({
            "text" : game.board
            }) 


        check = Gomoku.checkWin(board["board"])
        if check!='0':
            dataToSend["myTurn"] = False    
            winGomokuGame(u)
            Group("gomoku-user-%s" % str(players[0].id)).send({
                "text" : json.dumps(dataToSend)
                })
            Group("gomoku-user-%s" % str(players[1].id)).send({
                "text" : json.dumps(dataToSend)
                })
        elif u== players[0]:
            dataToSend["myTurn"] = False
            Group("gomoku-user-%s" % str(players[0].id)).send({
                "text" : json.dumps(dataToSend)
                })
            dataToSend["myTurn"] = True
            Group("gomoku-user-%s" % str(players[1].id)).send({
                "text" : json.dumps(dataToSend)
                })
        elif u==players[1]:
            dataToSend["myTurn"] = True
            Group("gomoku-user-%s" % str(players[0].id)).send({
                "text" : json.dumps(dataToSend)
                })
            dataToSend["myTurn"] = False
            Group("gomoku-user-%s" % str(players[1].id)).send({
                "text" : json.dumps(dataToSend)
                })

    


    
@channel_session_user    
def gomoku_ws_disconnect(message):
    if not message.user.is_authenticated():
        return
    
    u = GomokuOnline.objects.get(user=message.user)
    u.online=False
    u.save()
    room = u.room
    playersOnlineHtml = playersOnline(message)
    gomokuRoomsHtml = gomokuRooms(message)
    data = {"playersOnlineHtml": playersOnlineHtml,
            "gomokuRoomsHtml" : gomokuRoomsHtml }
    
    Group("gomoku").send({
    "text" : json.dumps(data)
    })
    Group("gomoku").discard(message.reply_channel)
    Group("gomoku-user-%s" % str(u.id)).discard(message.reply_channel)
    if room!= None:
        Group("gomoku-room-%s" % str(room.id)).discard(message.reply_channel)
    if u.currentGame != None:
        loseGomokuGame(u)
