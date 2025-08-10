"""
Tic Tac Toe Player
"""

import math
import random

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
    #x turn first if in ini state
    if board == initial_state():
        return X
    
    # Next count nums of x n O
    count_x, count_y = 0, 0
    
    count_x = sum(row.count(X) for row in board)
    count_y = sum(row.count(O) for row in board)
        
    if count_x == count_y:
        return X
    else: 
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_values = set()
    occupied = [X, O]

    for i, row in enumerate(board):
        for j, cell in enumerate(board):
            if board[i][j] not in occupied:
                possible_values.add((i, j))

    return possible_values



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    occupied = [X, 0]
    move = action

    turn = player(board)

    #deep copy
    new_board = []
    for row in board:
        new_row =  []
        for cell in row:
            new_row.append(cell)
        new_board.append(new_row)

    #checking for invalid states
    i, j = 0, 0
    i, j = move[0], move[1]
    if new_board[i][j] in occupied or i < 0 or j < 0: 
        raise Exception('Invalid State.')
    else:
        new_board[i][j] = turn
        return new_board
             

def winner(board):
    """
    Returns the winner of the game, if there is one.

    Win States:
    - diagonal (0,0), (1,1), (2,2) or (0,2), (1, 1), (2, 0)
    -  straight, up-down (0,0), (0,1), (o, 3)
    """

    for row in board:
        #first check straight
        if row == [X, X, X]:
            return X
        elif row == [O, O, O]:
            return O

    for i in range(3):
        if board[0][i] == X and board[1][i] == X and board[2][i] == X:
            return X
        elif board[0][i] == O and board[1][i] == O and board[2][i] == O:
            return O

    #diagonals - L_R
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    elif board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O

    if board[0][2] == X  and board[1][1] == X and board[2][0] == X:
        return X
    elif board[0][2] == O  and board[1][1] == O  and board[2][0] == O:
        return O
        
        
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board):
        return True
    
    count = 0
    for row in board:
        for cell in row:
            if cell  in [X, O]:
                count += 1

    if count == 9: return True
    return False

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

    def Min(board):
        v = float('inf')
        best_move = {}
        
        if terminal(board):
            return (utility(board), None)

        for action in actions(board):
            score, _ = Max(result(board, action))
            if score < v:
                v = score
                best_move = action
        
        return (v, best_move)
        

    def Max(board):
        v = float('-inf')
        best_move = {None}
        
        if terminal(board):
            return (utility(board), None)
        

        for action in actions(board):
            score, _ = Min(result(board, action))
            if score > v:
                v = score
                best_move = action
        
        return (v, best_move)

    turn = player(board)
    
    if terminal(board):
        return None
    
    action = None
    if turn == X:
        #try to max the score and opp will try to min it
        action = Max(board)
        return action[1]
    else:
        action = Min(board)
        return action[1]

def random_move(board):
    """
    Returns a random action for the current player on the board.
    """
    possible_moves = actions(board)
    if not possible_moves:
        return None
    return random.choice(list(possible_moves))