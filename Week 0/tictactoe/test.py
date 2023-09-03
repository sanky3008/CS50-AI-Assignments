import tictactoe as ttt

X = "X"
O = "O"
EMPTY = None

state = [[X, X, O],
        [O, X, O],
        [X, EMPTY, O]]

print(ttt.utility(state))