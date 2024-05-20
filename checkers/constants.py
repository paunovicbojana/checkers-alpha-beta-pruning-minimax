import pygame

WIDTH, HEIGHT = 500, 500
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

BROWN = (109, 79, 54)
WHITE = (240, 231, 202)
BLACK = (55, 30, 15)
BEIGE = (188, 170, 129)
GREEN = (14, 114, 37)

def get_color(color):
    if color == (55, 30, 15):
        return "CRNI"
    else: 
        return "BELI"

CROWN = pygame.transform.scale(pygame.image.load("assets/crown.png"), (30, 15))
