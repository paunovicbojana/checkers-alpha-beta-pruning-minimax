from .constants import *
from cmath import inf

def minimax(board, depth, alpha, beta, maximizing_player, game):
    if depth == 0 or game.game_over:
        return board.evaluate(), board

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in game.get_all_moves(board, BLACK):
            evaluation = minimax(move, depth - 1, alpha, beta, False, game)[0]
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in game.get_all_moves(board, WHITE):
            evaluation = minimax(move, depth - 1, alpha, beta, True, game)[0]
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval, best_move
