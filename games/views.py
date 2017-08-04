from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from .models import Chat, GomokuOnline, Message, Room, GomokuGame
from .models import BridgeChat, BridgeOnline, BridgeMessage, BridgeRoom, BridgeGame
from django.db.models import Count
import json
from channels import Channel, Group
from games.gomoku.gomoku import *
from games.gomoku.functions import *
from games.bridge.functions import *
from games.bridge.bridge import *
from random import shuffle

# Create your views here.



class GomokuView(View):
    template_name = 'games/gomoku_game.html'
    
    def get(self,request):
        """
        GET request
        :param u: current player in the gomoku game (model GomokuOnline)
        """
        data = {}
        if not self.request.user.is_authenticated():
            return redirect('mainPage:index')
        elif self.request.user.is_authenticated():
            u = GomokuOnline.objects.filter(user=self.request.user)
            if u.exists():
                u = get_object_or_404(GomokuOnline,user=self.request.user)
                #u = GomokuOnline.objects.get(user=self.request.user)
                u.online=True
                if (u.playing == False) and (u.readyToPlay==False) and (u.wantToPlay == False):
                    u.room=None
                u.save()
                
            else:
                u = GomokuOnline(user=self.request.user,online=True)
                u.room=None
                u.save()
            data['room'] = u.room
        return render(request,self.template_name,data)

class GomokuGameView(View):
    template_name = 'games/tic_tac_toe.html'
    
    def get(self,request):
        if not self.request.user.is_authenticated():
            return redirect('mainPage:index')        
        elif self.request.user.is_authenticated():
            u = get_object_or_404(GomokuOnline,user=self.request.user)
            #u = GomokuOnline.objects.get(user=self.request.user)
            if u.playing or u.readyToPlay or u.wantToPlay:
                return redirect('games:gomokuJoinGame',room_id=u.room.id)
            
            try:
                room = Room.objects.annotate(Count('gomokuonline', distinct=True)).filter(gomokuonline__count=0)[:1].get()
            except Room.DoesNotExist:
                room = Room()                
                room.save()
                chat = Chat()
                chat.room=room
                chat.save()
                u.room=room
                u.save()
        return redirect('games:gomokuJoinGame',room_id=room.id)
    
class GomokuJoinGameView(View):

    template_name = 'games/tic_tac_toe.html'
    
    def get(self,request,room_id):

        if not self.request.user.is_authenticated():
            return redirect('mainPage:index')        
        elif self.request.user.is_authenticated():
            u = get_object_or_404(GomokuOnline,user=self.request.user)            
            #u = GomokuOnline.objects.get(user=self.request.user)
            room_id = int(room_id)
            if u.playing or u.readyToPlay or u.wantToPlay:
                if room_id != u.room.id:
                    return redirect('games:gomokuJoinGame',room_id=u.room.id)                    
            room = get_object_or_404(Room, id=room_id)
            u.room=room
            u.save()
            namePlayer = ["Player1", "Player2", "Player3", "Player4"]
            
            players = GomokuOnline.objects.filter(room=room,wantToPlay=True)
            i=0
            
            for player in players:
                namePlayer[i]= player.user.username
                i+=1
        
        return render(request,self.template_name,{'n' : range(15), 'namePlayer1': namePlayer[0], 'namePlayer2': namePlayer[1], 'room': room, 'u' : u})   
     
class GomokuGameBoardView(View):
    def get(self,request):

        if not self.request.user.is_authenticated():
            return JsonResponse({})       
        if self.request.user.is_authenticated():
            u = get_object_or_404(GomokuOnline,user=self.request.user)            
            #u = GomokuOnline.objects.get(user=self.request.user)
            data = {}
            room=u.room
            
            players = GomokuOnline.objects.filter(room=room,wantToPlay=True)
            
            i=0
            namePlayer = ["Player1", "Player2", "Player3", "Player4"]
            data['player1Button'] = True
            data['player2Button'] = True
            data.update({"namePlayer1" : "Player1"})
            data.update({"namePlayer2" : "Player2"})
            for player in players:
                namePlayer[i]= player.user.username
                if i==0:
                    data.update({"namePlayer1" : player.user.username})
                    data['player1Button'] = False
                    if u==player:
                        data['player1Button'] = True
                if i==1:
                    data.update({"namePlayer2" : player.user.username})
                    data['player2Button'] = False
                    if u==player:
                        data['player2Button'] = True                    
                i+=1
            
            if not room.arePlaying:
                if players.count() == 2:
                    if u in players:
                        data['startButton'] = True
                        data['startButtonName'] = 'Start'
                        if u.readyToPlay:
                            data['startButtonName'] = 'Ready'
                    if players[0].readyToPlay and players[1].readyToPlay:
                        players[0].readyToPlay = False
                        players[1].readyToPlay = False                    
                        players[0].playing = True
                        players[1].playing = True
                        data['startButton'] = False
                        data['player1Button'] = False
                        data['player2Button'] = False
                        data['startButtonName'] = 'Playing' 
                        players[0].save()
                        players[1].save()               
                        room.arePlaying = True
                        room.save()
                        game = GomokuGame(room=room,board="{}",gameFinished=False)
                        game.save()
                        players[0].currentGame = game
                        players[1].currentGame = game
                        players[0].save()
                        players[1].save() 
                        board = json.loads(game.board)
                        if board == {}:
                            board["board"] = []
                            Gomoku.fillEmptyBoard(board["board"])
                        game.board = json.dumps(board)
                        game.save()
                        
                        dataToSend = {}
                        dataToSend["board"] = board["board"]
                        Group("gomoku-room-%s" % str(room.id)).send({
                            "text" : json.dumps(dataToSend)
                            })
                        dataToSend["myTurn"] = True
                        Group("gomoku-user-%s" % str(players[0].id)).send({
                            "text" : json.dumps(dataToSend)
                            })
                        dataToSend["myTurn"] = False
                        Group("gomoku-user-%s" % str(players[1].id)).send({
                            "text" : json.dumps(dataToSend)
                            })
                elif u in players:
                    data['startButton'] = False
                    data['startButtonName'] = 'Start'
                    u.readyToPlay=False
                    u.save()
                else:
                    data['startButton'] = False
                    data['startButtonName'] = 'Start'           
            elif room.arePlaying:
                data['startButton'] = False
                data['player1Button'] = False
                data['player2Button'] = False
                data['startButtonName'] = 'Playing'
            
            data['playerResign'] = False
               
            if u.room.arePlaying and u in players:
                data['playerResign'] = True
                

        return JsonResponse(data)   

#     def post(self,request):
#         if not self.request.user.is_authenticated():
#             return JsonResponse({})
#         u = get_object_or_404(GomokuOnline,user=self.request.user)
#         room= u.room
#         data = {}
# #         if room.arePlaying and ((room.firstPlayer==u.user) or (room.secondPlayer==u.user)):
# #             game = u.currentGame
# #             board = json.loads(game.board)
# #             if board == {}:
# #                 board["board"] = []
# #                 Gomoku.fillEmptyBoard(board["board"])
# #                 board["isFirstPlayer"] = True
# #                 
#  
#            
#             
#         
#         return JsonResponse(data)        
        

class GomokuStartGameView(View):

    def post(self,request):
        """
        POST request
        :param u: first player
        :param u2: second player
        """
        if not self.request.user.is_authenticated():
            return JsonResponse({})
        u = get_object_or_404(GomokuOnline,user=self.request.user)        
        #u = GomokuOnline.objects.get(user=self.request.user)
        room = u.room
        buttonPlayer1 = request.POST.get("buttonPlayer1",False) == 'true'
        buttonPlayer2 = request.POST.get("buttonPlayer2",False) == 'true'
        readyToPlay = request.POST.get("readyToPlay",False) == 'true'
        resign = request.POST.get("resign",False) == 'true'
        data ={}
        players = GomokuOnline.objects.filter(room=room,wantToPlay=True)
        if not room.arePlaying: 
            if buttonPlayer1 and u.wantToPlay==False:
                    u.wantToPlay=True
                    u.save()
            elif buttonPlayer1 and u.wantToPlay:
                u.wantToPlay=False
                u.readyToPlay=False
                u.save()
            if buttonPlayer2 and u.wantToPlay==False:
                    u.wantToPlay=True
                    u.save()
            elif buttonPlayer2 and u.wantToPlay:
                u.wantToPlay=False
                u.readyToPlay=False
                u.save()   
            if readyToPlay and players.count()==2:
                if u in players:
                    if u.readyToPlay==True:
                        u.readyToPlay=False
                    else:
                        u.readyToPlay=True
                    u.save()
        elif room.arePlaying:
            if u in players and resign:
                game = u.currentGame
                game.gameFinished = True
                losses = u.losses
                losses = losses+1
                u.losses = losses
                u.currentGame = None
                
                if players[0]!=u:
                    u2 = players[0]
                elif players[1]!=u:
                    u2 = players[1]
                wins = u2.wins
                wins = wins+1
                u2.wins = wins
                u2.currentGame = None
                u.playing = False
                u2.playing = False
                room.arePlaying = False
                u.save()                
                u2.save()
                game.save()
                room.save()
        return JsonResponse({})
        
           

class PlayerInGame(View):

    def get(self,request):
        """
        GET request
        :param u: list of the players online (model GomokuOnline)
        """
        if not self.request.user.is_authenticated():
            return HttpResponse('Please log in')
        u = GomokuOnline.objects.filter(online=True)
        return render(request, 'games/current_players_online.html', {'usersOnline': u})

class GomokuRooms(View):
    """
    display list of the rooms
    """
    def get(self,request):
        """
        GET request
        :param r: list of the rooms
        """
        if not self.request.user.is_authenticated():
            return HttpResponse('Please log in')
        r = Room.objects.annotate(Count('gomokuonline', distinct=True)).filter(gomokuonline__count__gt=0)
        return render(request, 'games/rooms.html', {'rooms': r})


class AddMessagesToChatView(View):

    def post(self,request):
        """
        POST request
        :param u: current player
        :param msg: message send by the user
        :param newMessage: new message saved in 'Message'
        """
        if not self.request.user.is_authenticated():
            return JsonResponse({})
        msg = request.POST.get('msgbox','')

        u = get_object_or_404(GomokuOnline,user=self.request.user)        
        #u = GomokuOnline.objects.get(user=request.user)
        if msg != '':
            newMessage = Message(user=self.request.user, message=msg)
            newMessage.chat=u.room.chat            
            newMessage.save()
            
        return JsonResponse({ })

class SendMessagesToUser(View):

    def get(self,request):
        """
        GET request
        :param m: messages assigned to the room
        """        
        if not self.request.user.is_authenticated():
            return HttpResponse('Please log in')
        u = get_object_or_404(GomokuOnline,user=self.request.user)
        #u = GomokuOnline.objects.get(user=request.user)
        m = Message.objects.filter(chat=u.room.chat)
        return render(request, 'games/messages.html', {'messages': m})



class BridgeView(View):

    template_name = 'games/bridge_game.html'
    
    def get(self,request):
        data = {}
        if not self.request.user.is_authenticated():
            return redirect('mainPage:index')
        elif self.request.user.is_authenticated():
            u = BridgeOnline.objects.filter(user=self.request.user)
            if u.exists():
                u = get_object_or_404(BridgeOnline,user=self.request.user)
                #u = GomokuOnline.objects.get(user=self.request.user)
                u.online=True
                if (u.playing == False) and (u.readyToPlay==False) and (u.wantToPlay == False):
                    u.room=None
                u.save()
                
            else:
                u = BridgeOnline(user=self.request.user,online=True)
                u.room=None
                u.save()
            data['room'] = u.room
        return render(request,self.template_name,data)

class BridgeGameView(View):
    """
    create new game
    """
    template_name = 'games/bridge.html'
    
    def get(self,request):
        if not self.request.user.is_authenticated():
            return redirect('mainPage:index')        
        elif self.request.user.is_authenticated():
            u = get_object_or_404(BridgeOnline,user=self.request.user)
            if u.playing or u.readyToPlay or u.wantToPlay:
                return redirect('games:bridgeJoinGame',room_id=u.room.id)
            
            try:
                room = BridgeRoom.objects.annotate(Count('bridgeonline', distinct=True)).filter(bridgeonline__count=0)[:1].get()
            except BridgeRoom.DoesNotExist:                      
                room = BridgeRoom()
                room.save()
                chat = BridgeChat()
                chat.room=room
                chat.save()
                u.room=room
                u.save()
        return redirect('games:bridgeJoinGame',room_id=room.id)
    
class BridgeJoinGameView(View):
    """
    join to the exist room
    """
    template_name = 'games/bridge.html'
    
    def get(self,request,room_id):
        if not self.request.user.is_authenticated():
            return redirect('mainPage:index')        
        elif self.request.user.is_authenticated():
            u = get_object_or_404(BridgeOnline,user=self.request.user)            
            #u = GomokuOnline.objects.get(user=self.request.user)
            room_id = int(room_id)
            if u.playing or u.readyToPlay or u.wantToPlay:
                if room_id != u.room.id:
                    return redirect('games:bridgeJoinGame',room_id=u.room.id)                    
            room = get_object_or_404(BridgeRoom, id=room_id)
            u.room=room
            u.save()
            namePlayer = ["Player1", "Player2", "Player3", "Player4"]
            
            players = BridgeOnline.objects.filter(room=room,wantToPlay=True)
            i=0
            
            for player in players:
                namePlayer[i]= player.user.username
                i+=1
        
        return render(request,self.template_name,{'n' : range(15), 'namePlayer1': namePlayer[0], 'namePlayer2': namePlayer[1], 'namePlayer3': namePlayer[2], 'namePlayer4': namePlayer[3], 'room': room, 'u' : u})   
     
class BridgeGameBoardView(View):
 
    def get(self,request):
        if not self.request.user.is_authenticated():
            return JsonResponse({})       
        if self.request.user.is_authenticated():
            u = get_object_or_404(BridgeOnline,user=self.request.user)            
            #u = GomokuOnline.objects.get(user=self.request.user)
            data = {}
            room=u.room
            
            players = BridgeOnline.objects.filter(room=room,wantToPlay=True)
            
            i=0
            #namePlayer = ["Player1", "Player2", "Player3", "Player4"]
            data['player1Button'] = True
            data['player2Button'] = True
            data['player3Button'] = True
            data['player4Button'] = True
            data.update({"namePlayer1" : "Player1"})
            data.update({"namePlayer2" : "Player2"})
            data.update({"namePlayer3" : "Player3"})
            data.update({"namePlayer4" : "Player4"})
            for player in players:
                #namePlayer[i]= player.user.username
                if i==0:
                    data.update({"namePlayer1" : player.user.username})
                    data['player1Button'] = False
                    if u==player:
                        data['player1Button'] = True
                if i==1:
                    data.update({"namePlayer2" : player.user.username})
                    data['player2Button'] = False
                    if u==player:
                        data['player2Button'] = True   
                if i==2:
                    data.update({"namePlayer3" : player.user.username})
                    data['player3Button'] = False
                    if u==player:
                        data['player3Button'] = True  
                if i==3:
                    data.update({"namePlayer4" : player.user.username})
                    data['player4Button'] = False
                    if u==player:
                        data['player4Button'] = True                                   
                i+=1
            
            if not room.arePlaying:
                if players.count() == 4:
                    if u in players:
                        data['startButton'] = True
                        data['startButtonName'] = 'Start'
                        if u.readyToPlay:
                            data['startButtonName'] = 'Ready'
                    if players[0].readyToPlay and players[1].readyToPlay and players[2].readyToPlay and players[3].readyToPlay:
                        players[0].readyToPlay = False
                        players[1].readyToPlay = False 
                        players[2].readyToPlay = False
                        players[3].readyToPlay = False                     
                        players[0].playing = True
                        players[1].playing = True
                        players[2].playing = True
                        players[3].playing = True
                        data['startButton'] = False
                        data['player1Button'] = False
                        data['player2Button'] = False
                        data['player3Button'] = False
                        data['player4Button'] = False
                        data['startButtonName'] = 'Playing' 
                        players[0].save()
                        players[1].save()
                        players[2].save()
                        players[3].save()
                                     
                        room.arePlaying = True
                        if room.turn=="West":
                            room.turn="North"
                        elif room.turn=="North":
                            room.turn="East"
                        elif room.turn=="East":
                            room.turn="South"
                        elif room.turn=="South":
                            room.turn="West"
                        
                        
                        
                        players[0].side="North"
                        players[1].side="East"
                        players[2].side="South"
                        players[3].side="West"
                        
                        room.save()
                        game = BridgeGame(room=room,board="{}",gameFinished=False)
                        game.save()
                        players[0].currentGame = game
                        players[1].currentGame = game
                        players[2].currentGame = game
                        players[3].currentGame = game
                        players[0].save()
                        players[1].save()
                        players[2].save()
                        players[3].save()
                        board = json.loads(game.board)
                        if board == {}:
                            board["turn"] = room.turn
                            board["suitGame"] = "A"
                            board["pointsAuction"] = 0
                            board["pointsNow"] = 0
                            allCards = [i for i in range(52) ]
                            shuffle(allCards)
                            board["cards"] = allCards
                            board["North"] = {}
                            board["East"] = {}
                            board["South"] = {}
                            board["West"] = {}
                            board["North"]["cards"] = allCards[0:13]
                            board["East"]["cards"] = allCards[13:26]
                            board["South"]["cards"] = allCards[26:39]
                            board["West"]["cards"] = allCards[39:52]
                            
                            board["North"]["cards"].sort()
                            board["East"]["cards"].sort()
                            board["South"]["cards"].sort()
                            board["West"]["cards"].sort()                          

                            board["North"]["playingCard"] = -1
                            board["East"]["playingCard"] = -1
                            board["South"]["playingCard"] = -1
                            board["West"]["playingCard"] = -1
                            
                            board["C"] = ["",""]
                            board["D"] = ["",""]
                            board["H"] = ["",""]
                            board["S"] = ["",""]
                            board["NT"] = ["",""]
                            board["countAuction"] = 0
                            board["winnerAuction"] = ""
                        game.board = json.dumps(board)
                        game.save()
                        dataToSend = {}
                        #dataToSend["cards"] = board["cards"]
                        
                        # North - 0-12, East - 13-25, South - 26-38,  West - 39-51
                        
                        
                        #print(dataToSend)
                        
                        
                        #Group("bridge-room-%s" % str(room.id)).send({
                        #    "text" : json.dumps(dataToSend)
                        #    })
                        
                        for player in players:
                            if player.side == board["turn"]:
                                dataToSend["auctionMove"] = True
                            else:
                                dataToSend["auctionMove"] = False
                                
                            dataToSend["cards"] = board[player.side]["cards"]    
#                             if player.side == "North":
#                                 dataToSend["cards"] = board["NorthCards"]
#                             elif player.side == "East":
#                                 dataToSend["cards"] = board["EastCards"]
#                             elif player.side == "South":
#                                 dataToSend["cards"] = board["SouthCards"]
#                             elif player.side == "West":
#                                 dataToSend["cards"] = board["WestCards"]
                            
                            dataToSend["sideGame"] = player.side   
                            Group("bridge-user-%s" % str(player.id)).send({
                                "text" : json.dumps(dataToSend)
                                })
                elif u in players:
                    data['startButton'] = False
                    data['startButtonName'] = 'Start'
                    u.readyToPlay=False
                    u.save()
                else:
                    data['startButton'] = False
                    data['startButtonName'] = 'Start'           
            elif room.arePlaying:
                data['startButton'] = False
                data['player1Button'] = False
                data['player2Button'] = False
                data['player3Button'] = False
                data['player4Button'] = False
                data['startButtonName'] = 'Playing'
            
            data['playerResign'] = False
               
            if u.room.arePlaying and u in players:
                data['playerResign'] = True
                
        return JsonResponse(data)   


class BridgeStartGameView(View):

    def post(self,request):
        if not self.request.user.is_authenticated():
            return JsonResponse({})
        u = get_object_or_404(BridgeOnline,user=self.request.user)        
        room = u.room
        buttonPlayer1 = request.POST.get("buttonPlayer1",False) == 'true'
        buttonPlayer2 = request.POST.get("buttonPlayer2",False) == 'true'
        buttonPlayer3 = request.POST.get("buttonPlayer3",False) == 'true'
        buttonPlayer4 = request.POST.get("buttonPlayer4",False) == 'true'
        readyToPlay = request.POST.get("readyToPlay",False) == 'true'
        resign = request.POST.get("resign",False) == 'true'
        data ={}
        players = BridgeOnline.objects.filter(room=room,wantToPlay=True)
        if not room.arePlaying: 
            if buttonPlayer1 and u.wantToPlay==False:
                    u.wantToPlay=True
                    u.save()
            elif buttonPlayer1 and u.wantToPlay:
                u.wantToPlay=False
                u.readyToPlay=False
                u.save()
            if buttonPlayer2 and u.wantToPlay==False:
                    u.wantToPlay=True
                    u.save()
            elif buttonPlayer2 and u.wantToPlay:
                u.wantToPlay=False
                u.readyToPlay=False
                u.save()
            if buttonPlayer3 and u.wantToPlay==False:
                    u.wantToPlay=True
                    u.save()
            elif buttonPlayer3 and u.wantToPlay:
                u.wantToPlay=False
                u.readyToPlay=False
                u.save()
            if buttonPlayer4 and u.wantToPlay==False:
                    u.wantToPlay=True
                    u.save()
            elif buttonPlayer4 and u.wantToPlay:
                u.wantToPlay=False
                u.readyToPlay=False
                u.save()         
            if readyToPlay and players.count()==4:
                if u in players:
                    if u.readyToPlay==True:
                        u.readyToPlay=False
                    else:
                        u.readyToPlay=True
                    u.save()
        elif room.arePlaying:
            if u in players and resign:
                game = u.currentGame
                game.gameFinished = True
            
                for player in players:
                    player.playing = False
                    player.currentGame = None

                    if player == u:
                        losses = player.losses
                        losses = losses+1
                        player.losses = losses
                    else:
                        wins = player.wins
                        wins = wins+1
                        player.wins = wins
                    player.save()
                room.arePlaying = False
                game.save()
                room.save()
        return JsonResponse({})
        
           


class AddMessagesToChatViewBridge(View):

    def post(self,request):
        if not self.request.user.is_authenticated():
            return JsonResponse({})
        msg = request.POST.get('msgbox','')

        u = get_object_or_404(BridgeOnline,user=self.request.user)        
        #u = GomokuOnline.objects.get(user=request.user)
        if msg != '':
            newMessage = BridgeMessage(user=self.request.user, message=msg)
            newMessage.chat=u.room.bridgechat            
            newMessage.save()
            
        return JsonResponse({ })

class SendMessagesToUserBridge(View):

    def get(self,request):

        if not self.request.user.is_authenticated():
            return HttpResponse('Please log in')
        u = get_object_or_404(BridgeOnline,user=self.request.user)
        #u = GomokuOnline.objects.get(user=request.user)
        m = BridgeMessage.objects.filter(chat=u.room.bridgechat)
        return render(request, 'games/messages.html', {'messages': m})



    