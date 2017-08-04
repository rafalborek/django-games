from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from games.models import Chat, GomokuOnline, Message, Room, GomokuGame
from django.db.models import Count
import json



        
        

def to_json(data,text):
    try:
        myjson = json.loads(text)
        data.update(myjson)
        print(data)
    except ValueError:
        return False
    return True

def playersOnline(message):
    if not message.user.is_authenticated():
        return 'Please log in'
    u = GomokuOnline.objects.filter(online=True)
    return render_to_string('games/current_players_online.html', {'usersOnline': u})


def gomokuRooms(message):
    if not message.user.is_authenticated():
        return 'Please log in'
    r = Room.objects.annotate(num_online=Count('gomokuonline', distinct=True)).filter(num_online__gt=0)
    return render_to_string('games/rooms.html', {'rooms': r})


def loseGomokuGame(u):
    room = u.room
    players = GomokuOnline.objects.filter(room=room,playing=True)
    if room.arePlaying:
        if u in players:
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

def winGomokuGame(u):
    room = u.room
    players = GomokuOnline.objects.filter(room=room,playing=True)
    if room.arePlaying:
        if u in players:
            game = u.currentGame
            game.gameFinished = True
            losses = u.losses
            losses = losses+1
    
            if players[0]!=u:
                u2 = players[0]
            elif players[1]!=u:
                u2 = players[1]
            wins = u.wins
            wins = wins+1
            u.wins = wins
            losses = u2.losses
            losses = losses+1
            u2.losses = losses
            u.currentGame = None
            u2.currentGame = None
            u.playing = False
            u2.playing = False
            room.arePlaying = False
            u.save()                
            u2.save()
            game.save()
            room.save()

