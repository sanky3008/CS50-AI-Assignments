"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x = sum(row.count(X) for row in board)
    o = sum(row.count(O) for row in board)

    if x == o:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    solution = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                solution.add((i,j))
    
    return solution

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    res = [row[:] for row in board]
    p = player(board)
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("invalid move")
    else:
        res[action[0]][action[1]] = p
        return res

def columns(board):
    col = []
    for i in range(3):
            col.append([board[0][i], board[1][i], board[2][i]])
    
    return col

def diagonal(board):
    return [[board[0][0], board[1][1], board[2][2]],[board[0][2], board[1][1], board[2][0]]]
    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    x = [X, X, X]
    o = [O, O, O]

    if x in board or x in columns(board) or x in diagonal(board):
        return X
    elif o in board or o in columns(board) or o in diagonal(board):
        return O
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    else:
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    return False    
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    mp = {}
    if terminal(board) == True:
        return None

    if player(board) == X:
        return maxvalue(board)[1]
    else:
        return minvalue(board)[1]

    
def maxvalue(board):
    v = -math.inf
    best_move = None
    if terminal(board) == True:
        return [utility(board), None]
    else:
        for action in actions(board):
            hypo = minvalue(result(board, action))[0]
            if hypo > v:
                v = hypo
                best_move = action
    return [v, best_move]

def minvalue(board):
    v = math.inf
    best_move = None
    if terminal(board) == True:
        return [utility(board), None]
    else:
        for action in actions(board):
            hypo = maxvalue(result(board, action))[0]
            if hypo < v:
                v = hypo
                best_move = action
    return [v, best_move]
