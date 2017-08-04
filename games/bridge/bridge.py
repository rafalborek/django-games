from random import shuffle
class Bridge():

    side = ["West","North","East","South"]
    
    
    
    @staticmethod
    def checkVictory(u,board):
        room = u.room
        players = BridgeOnline.objects.filter(room=room,playing=True)
        game = u.currentGame
        

    @staticmethod
    def nextTurnBoard(board):
        if board["turn"]=="West":
            board["turn"]="North"
        elif board["turn"]=="North":
            board["turn"]="East"
        elif board["turn"]=="East":
            board["turn"]="South"
        elif board["turn"]=="South":
            board["turn"]="West"
