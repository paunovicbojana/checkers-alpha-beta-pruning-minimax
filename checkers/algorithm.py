from .constants import *
from cmath import inf

def minimax(board, depth, maximizing_player, game):
    if depth == 0 or game.game_over:
        winner = game.get_winner()
        if winner:
            game.game_over = True
        return board.evaluate(), board

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in game.get_all_moves(board, BLACK, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in game.get_all_moves(board, WHITE, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
        return min_eval, best_move
