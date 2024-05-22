from .constants import *
from time import time
'''
def minimax(board, depth, alpha, beta, maximizing_player, game):
    if depth == 0 or game.game_over or time() - game.start_time > 2.9:
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

'''
def minimax(board, depth, alpha, beta, maximizing_player, game, transposition_table):
    if board is None:
        return None, None
    transposition_entry = transposition_table.lookup(board)
    if transposition_entry is not None and transposition_entry.depth >= depth:
        return transposition_entry.value, transposition_entry.best_move
    if depth == 0 or game.game_over or time() - game.start_time > 2.9:
        return board.evaluate(), board

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in game.get_all_moves(board, BLACK, transposition_table):
            evaluation = minimax(move, depth - 1, alpha, beta, False, game, transposition_table)[0]
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        transposition_table.store(board, max_eval, depth, best_move)
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in game.get_all_moves(board, WHITE, transposition_table):
            evaluation = minimax(move, depth - 1, alpha, beta, True, game, transposition_table)[0]
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        transposition_table.store(board, min_eval, depth, best_move)
        return min_eval, best_move
