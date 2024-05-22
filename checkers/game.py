import pygame
from checkers.constants import *
from .board import Board
from copy import deepcopy

class Game:
    def __init__(self, window):
        self.window = window
        self.reset_board()

    def reset_board(self):
        self.board = Board()
        self.game_over = None
        self.turn = WHITE
        self.selected_piece = None
        self.valid_moves = {}
        self.tie = False
        self.winner = None

    def get_board(self):
        return self.board
    
    def get_winner(self):
        return self.winner
    
    def set_winner(self, winner):
        self.winner = winner

    def update_board(self):
        self.get_board().draw_total_board(self.window)
        if self.selected_piece:
            self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def select_piece(self, row, col):
        if self.selected_piece and (row, col) in self.valid_moves:
            result = self.move_piece(row, col)
            if not result:
                self.selected_piece = None
                return self.select_piece(row, col)
            return True
        if 0 <= row < ROWS and 0 <= col < COLS:
            piece = self.board.get_piece(row, col)
            
            if piece and piece.color == self.turn:
                self.selected_piece = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                return True

        return False

    def move_piece(self, row, col):
        cell = self.board.get_piece(row, col)
        if self.selected_piece and cell == 0 and (row, col) in self.valid_moves:
            self.board.move_piece_on_board(self.selected_piece, row, col)
            eaten = self.valid_moves[(row, col)]
            if eaten:
                self.board.remove_pieces(eaten)
            self.change_player()
            winner = self.get_winner()
            if winner is not None:
                self.game_over = True
            return True
        return False

    def change_player(self):
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.window, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def computer_move(self, board, transposition_table):
        self.board = board
        all_moves_b = self.get_all_moves(self.board, self.turn, transposition_table)
        self.change_player()
        
        all_moves = self.get_all_moves(self.board, self.turn, transposition_table)
        if len(all_moves) == 0 and len(all_moves_b) == 0:
            self.tie = True
            self.game_over = True
            pygame.time.delay(3000)
            return True
        if len(all_moves) == 0 and (self.board.black_pieces < self.board.white_pieces):
            self.set_winner(WHITE)
            self.game_over = True
            pygame.time.delay(3000)
            return True
        if len(all_moves) == 0 and (self.board.black_pieces > self.board.white_pieces):
            self.set_winner(BLACK)
            self.game_over = True
            pygame.time.delay(3000)
            return True
        
        
        winner = self.get_winner()
        if winner:
            self.game_over = True
            pygame.time.delay(5000)
        return True
    
    def get_all_moves(self, board, color, transposition_table):
        moves = []
        for piece in board.get_all_pieces(color):
            valid_moves = board.get_valid_moves(piece)
            
            for move, skip in valid_moves.items():
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_board = self.simulate_move(temp_piece, move, temp_board, skip)
                transposition_entry = transposition_table.lookup(new_board)
                
                if transposition_entry:
                    moves.append((transposition_entry.best_move, len(skip)))
                else:
                    moves.append((new_board, len(skip)))
                
        moves.sort(key=lambda x: x[1], reverse=True)
        return [move[0] for move in moves]

    def simulate_move(self, piece, move, board, skip):
        board.move_piece_on_board(piece, move[0], move[1])
        if skip:
            board.remove_pieces(skip)
        return board