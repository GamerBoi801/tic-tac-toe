import pygame
import sys
import time
import random
import tictactoe as ttt

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
x_color = (230, 70, 70)     # Red for X
o_color = (70, 150, 230)    # Blue for O
tile_hover = (255, 100, 100) #intense red for hover

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tic-Tac-Toe")

# Fonts
mediumFont = pygame.font.Font("assets/OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("assets/OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("assets/OpenSans-Regular.ttf", 60)

user = None
board = ttt.initial_state()
ai_turn = False

def draw_gradient_background(color_top, color_bottom):
    """Draw vertical gradient background."""
    for y in range(height):
        r = color_top[0] + (color_bottom[0] - color_top[0]) * y // height
        g = color_top[1] + (color_bottom[1] - color_top[1]) * y // height
        b = color_top[2] + (color_bottom[2] - color_top[2]) * y // height
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

def draw_button(rect, text, base_color, hover_color):
    """Draw a rounded button with hover effect."""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    color = hover_color if rect.collidepoint(mouse) else base_color
    pygame.draw.rect(screen, color, rect, border_radius=8)
    label = mediumFont.render(text, True, black)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)
    return click and rect.collidepoint(mouse)

def draw_tile(rect, symbol=None, hover=False):
    """Draw a tile with optional symbol and hover effect."""
    pygame.draw.rect(screen, white, rect, border_radius=8, width=3)
    if hover:
        pygame.draw.rect(screen, tile_hover, rect, 5, border_radius=8)
    if symbol:
        color = x_color if symbol == "X" else o_color
        move = moveFont.render(symbol, True, color)
        moveRect = move.get_rect(center=rect.center)
        screen.blit(move, moveRect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    draw_gradient_background((30, 30, 60), (60, 60, 120))

    # Let user choose a player
    if user is None:
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect(center=(width / 2, 50))
        screen.blit(title, titleRect)

        playXButton = pygame.Rect(width / 8, height / 2, width / 4, 50)
        playOButton = pygame.Rect(5 * (width / 8), height / 2, width / 4, 50)

        if draw_button(playXButton, "Play as X", white, tile_hover):
            time.sleep(0.2)
            user = ttt.X
        if draw_button(playOButton, "Play as O", white, tile_hover):
            time.sleep(0.2)
            user = ttt.O

    else:
        # Draw game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        mouse = pygame.mouse.get_pos()

        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                hover = rect.collidepoint(mouse) and board[i][j] == ttt.EMPTY
                draw_tile(rect, board[i][j], hover)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        # Show title
        if game_over:
            winner = ttt.winner(board)
            title_text = "Game Over: Tie." if winner is None else f"Game Over: {winner} wins."
        elif user == player:
            title_text = f"Play as {user}"
        else:
            dots = int(time.time() * 2) % 4
            title_text = f"Computer thinking{'.' * dots}"

        title = largeFont.render(title_text, True, white)
        titleRect = title.get_rect(center=(width / 2, 30))
        screen.blit(title, titleRect)

        # AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # User move
        if pygame.mouse.get_pressed()[0] and user == player and not game_over:
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse):
                        board = ttt.result(board, (i, j))

        # Play again
        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            if draw_button(againButton, "Play Again", white, tile_hover):
                time.sleep(0.2)
                user = None
                board = ttt.initial_state()
                ai_turn = False

    pygame.display.flip()
