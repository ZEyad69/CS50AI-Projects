"""
Tic Tac Toe Player
"""

import math
import copy
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
    count_x=0
    count_o=0
    for i in range(3):
        for j in range(3):
            if board[i][j]==X:
                count_x+=1
            elif board[i][j]==O:
                count_o+=1
    if count_x>count_o:
        return O
    else:
        return X
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves=set()
    for i in range(3):
        for j in range(3):
            if board[i][j]==EMPTY:
                moves.add((i,j))
    return moves

    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    if action not in actions(board):
        raise Exception("Invalid action")

    new_board = copy.deepcopy(board)
    current_player = player(board)
    action_i, action_j = action
    new_board[action_i][action_j] = current_player
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != EMPTY:
            return board[0][j]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board)==True:
        return None

    current_player=player(board)

    def max_value(board):
        if terminal(board):
            return utility(board)
        v=-math.inf
        for action in actions(board):
            v=max(v,min_value(result(board,action)))
        return v

    def min_value(board):
        if terminal(board):
            return utility(board)
        v=math.inf
        for action in actions(board):
            v=min(v,max_value(result(board,action)))
        return v

    if current_player==X:
        best_value=-float('inf')
        best_action=None   
        for action in actions(board):
            value=min_value(result(board,action))
            if value>best_value:
                best_value=value
                best_action=action
        return best_action
    else:
        best_value=float('inf')
        best_action=None
        for action in actions(board):
            value=max_value(result(board,action))
            if value<best_value:
                best_value=value
                best_action=action
        return best_action


  
