import matplotlib.pyplot as plt
import numpy as np

plt.close('all')

moveable = [[5,i] for i in range(7)]

board = np.zeros((6,7))

x = [i for i in range(7)]
y = [i for i in range(6)]
xx,yy = np.meshgrid(x,y)

player = 1

# def move(x,player,moveable,board = board,checkscore = True):
#     column = int(x+0.5)

#     if moveable[column][0] < 0:
#         print('Not valid')
#         return #-player*np.inf

#     board[moveable[column][0],moveable[column][1]] = player

#     if checkscore:
#         score = checkwin((moveable[column][0],moveable[column][1]),player,board)
#         return score

#     # if moveable[column][0] - 1 < 0:
#     #     moveable.pop
#     moveable[column][0] -= 1

def moveablesFunc(board):
    heights = np.sum(board != 0, axis=0)
    return [(5 - h,i) for i,h in enumerate(heights) if 5-h >= 0]


def scoreFunc(pos,player,board):
    r, c = pos
    row = board[r]
    column = board[:,c]
    diag1 = board.diagonal(c-r)
    diag2 = board[:,::-1].diagonal((6-c)-r)

    d1loc = min(r,c)
    d2loc = min(r,6-c)
    twos,threes,fours = [], [], []
    
    for i in range(2):
        twos.append(row[c-i:c-i+2])
        twos.append(column[r-i:r-i+2])
        twos.append(diag1[d1loc-i:d1loc-i+2])
        twos.append(diag2[d2loc-i:d2loc-i+2])
    for i in range(3):
        threes.append(row[c-i:c-i+3])
        threes.append(column[r-i:r-i+3])
        threes.append(diag1[d1loc-i:d1loc-i+3])
        threes.append(diag2[d2loc-i:d2loc-i+3])
    for i in range(4):
        fours.append(row[c-i:c-i+4])
        fours.append(column[r-i:r-i+4])
        fours.append(diag1[d1loc-i:d1loc-i+4])
        fours.append(diag2[d2loc-i:d2loc-i+4])
    
    stwos = list(map(sum,twos))
    sthrees = list(map(sum,threes))
    sfours = list(map(sum,fours))

    stwo = sum(np.asarray(stwos) == 2*player)
    sthree = sum(np.asarray(sthrees) == 3*player)
    sfour = sum(np.asarray(sfours) == 4*player)

    score = player*(20*sfour + 6*sthree + 3*stwo)
    return score


def search(player,depth):
    moveables = moveablesFunc(board)
    for pos in moveables:
        board[pos[0],pos[1]] = player
        print(pos, search2(pos,player,depth))
        board[pos[0],pos[1]] = 0

def search2(pos,player,depth,alpha=-np.inf,beta=np.inf):
    moveables = moveablesFunc(board)

    if depth <= 0 or len(moveables) == 0:
        # score = scoreFunc(pos,-player,board)
        score = 0
        for row, col in zip(yy[board == -player],xx[board == -player]):
            score += scoreFunc((row,col),-player,board)
        for row, col in zip(yy[board == player],xx[board == player]):
            score += scoreFunc((row,col),player,board)
        return score
    
    maximizing = player == 1

    if maximizing:
        value = -np.inf
        for pos in moveables:
            board[pos[0],pos[1]] = player
            value = max(value,search2(pos,-player,depth-1,alpha,beta))
            board[pos[0],pos[1]] = 0
            alpha = max(alpha,value)
            if alpha >= beta:
                # print('alpha break')
                break
        return value
    else:
        value = np.inf
        for pos in moveables:
            board[pos[0],pos[1]] = player
            value = min(value,search2(pos,-player,depth-1,alpha,beta))
            board[pos[0],pos[1]] = 0
            beta = min(beta,value)
            if beta <= alpha:
                # print('beta break')
                break
        return value


def onclick(event):
    global player
    moveables = np.array(moveablesFunc(board))
    col = int(event.xdata + 0.5)
    pos = moveables[moveables[:,1] == col][0]
    try:
        board[pos[0],pos[1]] = player
    except:
        print("Invalid move")
        return

    yellow.set_offsets(np.array([xx[board == 1],yy[board == 1]]).T)
    red.set_offsets(np.array([xx[board == -1], yy[board == -1]]).T)

    player *= -1
    ax.set_title(f"player {player}'s turn. 1: Yellow, -1: Red")

    fig.canvas.draw()


fig, ax = plt.subplots(figsize=(8,8))
ax.set(xlim=(-1,7),ylim=(-1,6),title=f"player {player}'s turn. 1: Yellow, -1: Red")
plt.gca().invert_yaxis()
radius = 2000

plate = ax.scatter(xx,yy,s=radius)
yellow = ax.scatter([],[],s=radius,c='yellow')    #player 1
red = ax.scatter([],[],s=radius,c='r')            #player -1

fig.show()

fig.canvas.mpl_connect('button_press_event',onclick)

# def search(pos,player,depth,alpha,beta,moveable):
#     # print(board)

#     if depth <= 0 or moveable[pos[1]][0] < 0:
#         print(board)
#         return checkwin(pos,player,board)
    
#     maximizing = player == 1
#     # move(pos[1],player,moveable,board,False)
#     moveable_copy = moveable.copy() 

#     if maximizing:
#         value = -np.inf
#         for pos in moveable:
#             origin_pos = pos.copy()
#             move(pos[1],player,moveable_copy,board,False)
#             value = max(value,search(pos,player*(-1),depth-1,alpha,beta,moveable_copy))
#             alpha = max(alpha,value)
#             # print(board)
#             board[origin_pos[0],origin_pos[1]] = 0
#             # print(board)
#             if alpha >= beta:
#                 break
            
#         return value
#     else:
#         value = np.inf
#         for pos in moveable:
#             origin_pos = pos.copy()
#             move(pos[1],player,moveable_copy,board,False)
#             value = min(value,search(pos,player*(-1),depth - 1,alpha,beta,moveable_copy))
#             beta = min(beta,value)
#             board[origin_pos[0],origin_pos[1]] = 0
#             if beta <= alpha:
#                 break
            
#         return value