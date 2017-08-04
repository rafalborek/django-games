from channels import Channel, Group
from channels.sessions import channel_session, enforce_ordering
from channels.asgi import get_channel_layer
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
from django.contrib.auth.models import User
from games.models import BridgeChat, BridgeOnline, BridgeMessage, BridgeRoom, BridgeGame
import json
from games.bridge.functions import *
from games.bridge.bridge import *
from games.gomoku.gomoku import *

@channel_session_user_from_http
def bridge_ws_connect(message):

    if not message.user.is_authenticated():
        return
    
    channel_layer = get_channel_layer()
    ch_group_list = channel_layer.group_channels('bridge')
    u = BridgeOnline.objects.get(user=message.user)
    u.online=True
    u.save()
    Group("bridge").add(message.reply_channel)
    Group("bridge-user-%s" % str(u.id)).add(message.reply_channel)
    playersOnlineHtml = playersOnlineBridge(message)
    bridgeRoomsHtml = bridgeRooms(message)
    data = {"playersOnlineHtml": playersOnlineHtml,
            "bridgeRoomsHtml" : bridgeRoomsHtml }
    
    Group("bridge").send({
    "text" : json.dumps(data)
    })
    

@channel_session_user
def bridge_ws_receive(message):

    if not message.user.is_authenticated():
        return
    data = {}
    if not to_json_bridge(data,message['text']):
        return
    
    u = BridgeOnline.objects.get(user=message.user)
    room = u.room
    
    
    if "inRoom" in data and room != None:
            Group("bridge-room-%s" % str(room.id)).add(message.reply_channel)
            bridgeRoomsHtml = bridgeRooms(message)
            toSend = {"bridgeRoomsHtml" : bridgeRoomsHtml }
            Group("bridge").send({
                "text" : json.dumps(toSend)
            })
            if room.arePlaying:
                player = BridgeOnline.objects.get(room=room,playing=True)[0]
                game = player.currentGame
                Group("bridge-room-%s" % str(room.id)).send({
                    "text" : game.board
                })
            return 
    
    # TODO: The gameplay does not work properly
    if "auctionMove" in data and u.playing:
        players = BridgeOnline.objects.filter(room=room,playing=True)
        game = u.currentGame
        board = json.loads(game.board)
        dataToSend = {}
        try:
            
            if u.side == board["turn"]:
                if "pass" in data:
                    board["countAuction"]+=1
                else:
                    print("Jestem tuuuuu : 1000")
                    pointsAuction = data["pointsAuction"]
                    suitAuction = data["suitAuction"]
                    if int(pointsAuction) > int(board["pointsAuction"]) and \
                    (suitAuction=="C" or suitAuction=="D" or suitAuction=="H" or suitAuction =="S" or suitAuction=="NT"):
                        board["pointsAuction"] = int(pointsAuction)
                        board["suitGame"] = suitAuction
                        if u.side == "North" or u.side == "South":
                            if board[board["suitGame"]][0]=="":
                                board[board["suitGame"]][0] =u.side
                            board["winnerAuction"] = board[board["suitGame"]][0]
                        elif u.side == "East" or u.side == "West":
                            if board[board["suitGame"]][1]=="":
                                board[board["suitGame"]][1]=u.side
                            board["winnerAuction"] = board[board["suitGame"]][1]                            
                        board["countAuction"]=1
                    elif int(pointsAuction)==int(board["pointsAuction"]) and board["suitGame"] != "NT" \
                    and (suitAuction>board["suitGame"] or suitAuction=="NT"):
                        board["pointsAuction"] = int(pointsAuction)
                        board["suitGame"] = suitAuction
                        if u.side == "North" or u.side == "South":
                            if board[board["suitGame"]][0]=="":
                                board[board["suitGame"]][0] =u.side
                            board["winnerAuction"] = board[board["suitGame"]][0]
                        elif u.side == "East" or u.side == "West":
                            if board[board["suitGame"]][1]=="":
                                board[board["suitGame"]][1]=u.side
                            board["winnerAuction"] = board[board["suitGame"]][1]                   
                        board["countAuction"]=1

                if board["turn"]=="West":
                    board["turn"]="North"
                elif board["turn"]=="North":
                    board["turn"]="East"
                elif board["turn"]=="East":
                    board["turn"]="South"
                elif board["turn"]=="South":
                    board["turn"]="West"
                    
                game.board = json.dumps(board)
                game.save()
                
                dataToSend["pointsAuction"] = board["pointsAuction"]
                dataToSend["suitGame"] = board["suitGame"]
                Group("bridge-room-%s" % str(room.id)).send({
                    "text" : json.dumps(dataToSend)
                })
                
                if (int(board["pointsAuction"])==7 and board["suitGame"] =="NT") or board["countAuction"]==4:
                    if int(board["pointsAuction"])==0:
                        loseBridgeGame(u)
                        return
                    board["turn"] = board["winnerAuction"]
                    game.board = json.dumps(board)
                    game.save()
                    
                    toSendData = {}
                    toSendData["winnerAuction"] = board["winnerAuction"]
                    if board["winnerAuction"] == "North":
                        toSendData["secondPlaying"] = "South"
                        toSendData["cardsSecond"] = board["South"]["cards"]
                    elif board["winnerAuction"] == "South":
                        toSendData["secondPlaying"] = "North"
                        toSendData["cardsSecond"] = board["North"]["cards"]
                    elif board["winnerAuction"] == "West":
                        toSendData["secondPlaying"] = "East"
                        toSendData["cardsSecond"] = board["East"]["cards"]
                    elif board["winnerAuction"] == "East":
                        toSendData["secondPlaying"] = "West"
                        toSendData["cardsSecond"] = board["West"]["cards"]
                         
                    Group("bridge-room-%s" % str(room.id)).send({
                        "text" : json.dumps(toSendData)
                    })                                                  
                    for player in players:
                        if board["turn"] == player.side:
                            dataToSend["myTurn"] = True
                        else:
                            dataToSend["myTurn"] = False
                        
                        dataToSend["auctionMove"] = False
                        
                        Group("bridge-user-%s" % str(player.id)).send({
                        "text" : json.dumps(dataToSend)
                        })
                else:                           
                    for player in players:
                        if board["turn"] == player.side:
                            dataToSend["auctionMove"] = True
                        else:
                            dataToSend["auctionMove"] = False
                        
                     
                        Group("bridge-user-%s" % str(player.id)).send({
                        "text" : json.dumps(dataToSend)
                        })        
                        
            else:
                return
        except:
            return
        
        
        
    if "move" in data and u.playing:
        
        
        
        players = BridgeOnline.objects.filter(room=room,playing=True)
        game = u.currentGame
        board = json.loads(game.board)
        
        if board["turn"] == u.side:
#             
#             if not board[u.side]["cards"]:
#                 pass
            if int(data["playingCard"]) in board[u.side]["cards"]:
                board[u.side]["playingCard"] = int(data["playingCard"])
            #TODO: check victory function
            if board["North"]["playingCard"] != -1 and board["East"]["playingCard"] != -1 \
            and board["South"]["playingCard"] != -1 and board["West"]["playingCard"] != -1:
                Bridge.checkVictory(u,board)
                
                
            for player in players:
                if board["turn"] == player.side:
                    dataToSend["myTurn"] = True
                else:
                    dataToSend["myTurn"] = False
                
                dataToSend["auctionMove"] = False
                Group("bridge-user-%s" % str(player.id)).send({
                "text" : json.dumps(dataToSend)
                })            
            


    
    
@channel_session_user    
def bridge_ws_disconnect(message):
    if not message.user.is_authenticated():
        return
    
    u = BridgeOnline.objects.get(user=message.user)
    u.online=False
    u.save()
    room = u.room
    playersOnlineHtml = playersOnlineBridge(message)
    bridgeRoomsHtml = bridgeRooms(message)
    data = {"playersOnlineHtml": playersOnlineHtml,
            "bridgeRoomsHtml" : bridgeRoomsHtml }
    
    Group("bridge").send({
    "text" : json.dumps(data)
    })
    Group("bridge").discard(message.reply_channel)
    Group("bridge-user-%s" % str(u.id)).discard(message.reply_channel)
    if room!= None:
        Group("bridge-room-%s" % str(room.id)).discard(message.reply_channel)
    if u.currentGame != None:
        loseBridgeGame(u)
