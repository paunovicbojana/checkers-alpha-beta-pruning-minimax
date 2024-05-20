import pygame
from .constants import *
from .piece import Piece
from copy import deepcopy

class Board:
    def __init__(self):
        self.board = []
        self.white_pieces = 12
        self.black_pieces = 12
        self.white_kings = 0
        self.black_kings = 0
        self.create_board()
        
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, BLACK))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, WHITE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw_cells(self, window):
        window.fill(BROWN)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, BEIGE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_total_board(self, window):
        self.draw_cells(window)
        for row in range(ROWS):
            for col in range(COLS):
                cell = self.board[row][col]
                if cell != 0:
                    cell.draw_piece(window)

    def remove_pieces(self, pieces):
        for piece in pieces:
            if piece != 0:
                self.board[piece.row][piece.col] = 0
                if piece.color == WHITE:
                    if piece.king:
                        self.white_kings -= 1
                    else: 
                        self.white_pieces -= 1
                elif piece.color == BLACK:
                    if piece.king:
                        self.black_kings -= 1
                    else: 
                        self.black_pieces -= 1

    def get_piece(self, row, col):
        return self.board[row][col]
    
    def winner(self):
        if self.black_pieces <= 0:
            return WHITE
        elif self.white_pieces <= 0:
            return BLACK
        return None
    
    def move_piece_on_board(self, piece, row, col, eaten=[]):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if eaten:
            self.remove_pieces(eaten)
        if (row == ROWS - 1 or row == 0) and not piece.king:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1

    def get_valid_moves(self, piece):
        moves = {}
        row = piece.row
        col = piece.col
        directions_black = [(1,-1), (1,1)]
        directions_white = [(-1,-1), (-1,1)]
        directions_king = [(1,-1), (1,1), (-1,-1), (-1,1)]
        if piece.king:
            moves.update(self.traverse(directions_king, row, col, piece))
        elif piece.color == WHITE:
            moves.update(self.traverse(directions_white, row, col, piece))
        elif piece.color == BLACK:
            moves.update(self.traverse(directions_black, row, col, piece))

        return moves

        
    def traverse(self, directions, row, col, piece):
        moves = {}
        for dr, dc in directions:
            possiable_row, possiable_col = row + dr, col + dc
            if 0 <= possiable_row < ROWS and 0 <= possiable_col < COLS:
                jumping_cell = self.board[possiable_row][possiable_col]
                if jumping_cell == 0:
                    moves[(possiable_row, possiable_col)] = []
                elif jumping_cell.color != piece.color:
                    new_possiable_row, new_possiable_col = possiable_row + dr, possiable_col + dc
                    if 0 <= new_possiable_row < ROWS and 0 <= new_possiable_col < COLS:
                        new_jumping_cell = self.board[new_possiable_row][new_possiable_col]
                        if new_jumping_cell == 0:
                            moves[(new_possiable_row, new_possiable_col)] = [jumping_cell]
                            self.multi_jump(new_possiable_row, new_possiable_col, piece, moves, [jumping_cell])

        return moves

    def multi_jump(self, row, col, piece, moves, skipped):
        directions_black = [(1, -1), (1, 1)]
        directions_white = [(-1, -1), (-1, 1)]
        directions_king = [(1,-1), (1,1), (-1,-1), (-1,1)]
        if piece.king:
            directions = directions_king
        elif piece.color == WHITE:
            directions = directions_white
        elif piece.color == BLACK:
            directions = directions_black

        for dr, dc in directions:
            possiable_row, possiable_col = row + dr, col + dc
            if 0 <= possiable_row < ROWS and 0 <= possiable_col < COLS:
                jumping_cell = self.board[possiable_row][possiable_col]
                if jumping_cell == 0:
                    continue
                if jumping_cell.color != piece.color and jumping_cell not in skipped:
                    new_possiable_row, new_possiable_col = possiable_row + dr, possiable_col + dc
                    if 0 <= new_possiable_row < ROWS and 0 <= new_possiable_col < COLS:
                        new_jumping_cell = self.board[new_possiable_row][new_possiable_col]
                        if new_jumping_cell == 0:
                            new_skipped = skipped + [jumping_cell]
                            moves[(new_possiable_row, new_possiable_col)] = new_skipped
                            self.multi_jump(new_possiable_row, new_possiable_col, piece, moves, new_skipped)
    
    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
    
    def evaluate(self):
        white_score = self.white_pieces + self.white_kings * 2
        black_score = self.black_pieces + self.black_kings * 2
        return black_score - white_score