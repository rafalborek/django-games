from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from games.models import BridgeChat, BridgeOnline, BridgeMessage, BridgeRoom, BridgeGame
from django.db.models import Count
import json



        
        

def to_json_bridge(data,text):
    try:
        myjson = json.loads(text)
        data.update(myjson)
        print(data)
    except ValueError:
        return False
    return True

def playersOnlineBridge(message):
    if not message.user.is_authenticated():
        return 'Please log in'
    u = BridgeOnline.objects.filter(online=True)
    return render_to_string('games/current_players_online.html', {'usersOnline': u})


def bridgeRooms(message):
    if not message.user.is_authenticated():
        return 'Please log in'
    r = BridgeRoom.objects.annotate(num_online=Count('bridgeonline', distinct=True)).filter(num_online__gt=0)
    return render_to_string('games/bridge_rooms.html', {'rooms': r})


def loseBridgeGame(u):
    room = u.room
    players = BridgeOnline.objects.filter(room=room,playing=True)
    if room.arePlaying:
        if u in players:
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

def winBridgeGame(u):
    room = u.room
    players = BridgeOnline.objects.filter(room=room,playing=True)
    if room.arePlaying:
        if u in players:
            game = u.currentGame
            game.gameFinished = True
        
            for player in players:
                player.playing = False
                player.currentGame = None

                if player == u:
                    wins = player.wins
                    wins += 1
                    player.wins = wins
                else:
                    losses = player.losses
                    losses = losses+1
                    player.losses = losses
                player.save()
            room.arePlaying = False
            game.save()
            room.save()

