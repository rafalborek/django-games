class Gomoku():
    @staticmethod
    def fillEmptyBoard(board):
        board.extend([['0' for x in range(15)] for y in range(15)]) 
    @staticmethod
    def makeMove(board,i,j,playerChar):
        if board[i][j]=='0':
            board[i][j]=playerChar
            return True
        return False
    @staticmethod
    def checkRow(board):
        countX=0
        countO=0
        for i in range(15):
            for j in range(15):
                if board[i][j] == 'x':
                    countX+=1
                    if countX==5:
                        if j==14 or board[i][j+1]!='x':
                            return 'x'
                        else:
                            j+=1
                            countX+=1
                    countO=0
                elif board[i][j] == 'o':
                    countO+=1
                    if countO==5:
                        if j==14 or board[i][j+1]!='o':
                            return 'o'
                        else:
                            j+=1
                            countO+=1
                    countX=0
                else:
                    countO=0
                    countX=0
        return '0'
            
            
                    
                
                    
                    
    @staticmethod
    def checkColumn(board):
        countX=0
        countO=0
        for j in range(15):
            for i in range(15):
                if board[i][j] == 'x':
                    countX+=1
                    if countX==5:
                        if j==14 or board[i][j+1]!='x':
                            return 'x'
                        else:
                            j+=1
                            countX+=1
                    countO=0
                elif board[i][j] == 'o':
                    countO+=1
                    if countO==5:
                        if j==14 or board[i][j+1]!='o':
                            return 'o'
                        else:
                            j+=1
                            countO+=1
                    countX=0
                else:
                    countO=0
                    countX=0
        return '0'
    
    @staticmethod
    def checkDiagonal(board):
        countX=0
        countO=0
        for i in range(15):
            for j in range(15):
                if (j+i)>14:
                    countO=0
                    countX=0
                    break
                if ((j+i)<15) and (board[j][j+i] == 'x'):
                    countX+=1
                    if countX==5:
                        if (j+i)==14 or board[j+1][j+1+i]!='x':
                            return 'x'
                        else:
                            j+=1
                            countX+=1
                    countO=0
                elif ((j+i)<15) and (board[j][j+i] == 'o'):
                    countO+=1
                    if countO==5:
                        if (j+i)==14 or board[j+1][i+j+1]!='o':
                            return 'o'
                        else:
                            j+=1
                            countO+=1
                    countX=0
                else:
                    countO=0
                    countX=0
        countO=0
        countX=0
        for i in range(15):
            for j in range(15):
                if (j+i)>14:
                    countO=0
                    countX=0
                    break
                if ((j+i)<15) and (board[j+i][j] == 'x'):
                    countX+=1
                    if countX==5:
                        if (i+j)==14 or board[i+j+1][j+1]!='x':
                            return 'x'
                        else:
                            j+=1
                            countX+=1
                    countO=0
                elif ((j+i)<15) and (board[j+i][j] == 'o'):
                    countO+=1
                    if countO==5:
                        if (i+j)==14 or board[i+j+1][j+1]!='o':
                            return 'o'
                        else:
                            j+=1
                            countO+=1
                    countX=0
                else:
                    countO=0
                    countX=0
                countX=0
        
        countO=0
        countX=0
        
        for i in range(15):
            for j in range(15):
                if (j+i)>14:
                    countO=0
                    countX=0
                    break
                if board[j][14-j-i] == 'x':
                    countX+=1
                    if countX==5:
                        if ((i+j)==14) or (board[j+1][14-j-1-i]!='x'):
                            return 'x'
                        else:
                            j+=1
                            countX+=1
                    countO=0
                elif board[j][14-j-i] == 'o':
                    countO+=1
                    if countO==5:
                        if ((i+j)==14) or (board[j+1][14-j-1-i]!='o'):
                            return 'o'
                        else:
                            j+=1
                            countO+=1
                    countX=0
                else:
                    countO=0
                    countX=0
        countO=0
        countX=0
        
        for i in range(15):
            for j in range(15):
                if (i+j)>14:
                    countO=0
                    countX=0
                    break
                if board[j+i][14-j] == 'x':
                    countX+=1
                    if countX==5:
                        if ((i+j)==14) or (board[j+i+1][14-j-1]!='x'):
                            return 'x'
                        else:
                            j+=1
                            countX+=1
                    countO=0
                elif board[j+i][14-j] == 'o':
                    countO+=1
                    if countO==5:
                        if ((i+j)==14) or (board[j+i+1][14-j-1]!='o'):
                            return 'o'
                        else:
                            j+=1
                            countO+=1
                    countX=0
                else:
                    countO=0
                    countX=0
        return '0'

    @staticmethod
    def checkWin(board):
        check = Gomoku.checkRow(board)
        if check!='0':
            return check
        check = Gomoku.checkColumn(board)
        if check!= '0':
            return check
        check = Gomoku.checkDiagonal(board)
        return check
    
       