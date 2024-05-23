import pygame
from checkers.constants import *
from checkers.game import Game
from checkers.algorithm import minimax
from checkers.hashing import TranspositionTable
from time import time

FPS = 60
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers Game')

def get_position_mouse(position):
    x, y = position
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def display_winner(window, winner):
    font = pygame.font.Font(None, 50)
    color_name = get_color(winner)
    text = font.render(f'{color_name} igrač je pobedio!', True, (255, 255, 255))
    window.fill((14, 114, 37))
    window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.flip()
    pygame.time.delay(3000)

def display_menu(window):
    font = pygame.font.Font(None, 50)
    text_caption = font.render('CHECKERS', True, (255, 255, 255))
    text = font.render('START GAME', True, (255, 255, 255))

    window.fill((0, 0, 0)) 

    button_rect = text.get_rect(center=(WIDTH // 2, 2* HEIGHT // 3))
    pygame.draw.rect(window, (14, 114, 37), button_rect.inflate(20, 20))
    window.blit(text_caption, (WIDTH//2 - text_caption.get_width()//2, HEIGHT//3 - text_caption.get_height()//2))
    window.blit(text, button_rect.topleft)
    pygame.display.flip()

    return button_rect

def main():
    pygame.init()
    pygame.font.init()
    run = True
    clock = pygame.time.Clock()
    game_started = False

    while not game_started and run:
        button_rect = display_menu(window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    game_started = True

    if not run:
        pygame.quit()
        return

    game = Game(window)
    transposition_table = TranspositionTable()
    game.update_board()

    while run:
        clock.tick(FPS)
        game.update_board()

        if game.turn == BLACK:
            game.start_time = time()
            value, new_board = minimax(game.get_board(), 5, float("-inf"), float("inf"), True, game, transposition_table)
            time_elapsed = time() - game.start_time
            print(f"Time elapsed: {time_elapsed}")
            if new_board is None:
                game.game_over = True
            else:
                game.computer_move(new_board, transposition_table)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                row, col = get_position_mouse(position)
                game.select_piece(row, col)

        if game.game_over:
            win = game.get_winner()
            display_winner(window, win)
            run = False
            continue

    pygame.quit()

if __name__ == "__main__":
    main()
