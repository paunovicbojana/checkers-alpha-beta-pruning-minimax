from .constants import *
import pygame
class Piece():
    PADDING = 5
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        
        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self): # centriram figuru
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True
    
    def move(self, row, col): # pomeram figuru na zadato polje
        self.row = row
        self.col = col
        self.calculate_position() #centriram je na tom polju
    
    def draw_piece(self, window):
        radius = SQUARE_SIZE // 2 - self.PADDING 
        # prozor, boja, koordinate, poluprecnik
        pygame.draw.circle(window, self.color, (self.x, self.y), radius) # crtanje figure
        # crtanje krune
        if self.king and self.color == WHITE:
            # slika, koordinate 
            window.blit(CROWN1, (self.x - CROWN1.get_width()//2, self.y - CROWN1.get_height()//2))
        if self.king and self.color == BLACK:
            window.blit(CROWN2, (self.x - CROWN2.get_width()//2, self.y - CROWN2.get_height()//2))


    def __str__(self):
        return "White" if self.color == WHITE else "Black"
    
    def __repr__(self):
        return str(self)