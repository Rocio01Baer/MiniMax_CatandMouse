import pygame
import random
import time
import sys
from pygame.locals import *

# Definición del tablero
class Board:
    def __init__(self, size):
        self.size = size
        self.cat_pos = (0, 0)  # Posición inicial del gato
        self.mouse_pos = (size-1, size-1)  # Posición inicial del ratón

# Función para obtener los vecinos de una posición en el tablero
def get_neighbors(position, size):
    x, y = position
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < size and 0 <= ny < size:
            neighbors.append((nx, ny))
    return neighbors

# Función para calcular la distancia de Manhattan entre dos posiciones
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Algoritmo Minimax
def minimax(board, depth, is_maximizing_player, alpha, beta):
    if depth == 0 or board.cat_pos == board.mouse_pos:
        return -manhattan_distance(board.mouse_pos, board.cat_pos) if is_maximizing_player else manhattan_distance(board.mouse_pos, board.cat_pos)

    if is_maximizing_player:
        max_eval = float('-inf')
        for move in get_neighbors(board.mouse_pos, board.size):
            original_pos = board.mouse_pos
            board.mouse_pos = move
            eval = minimax(board, depth-1, False, alpha, beta)
            board.mouse_pos = original_pos
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_neighbors(board.cat_pos, board.size):
            original_pos = board.cat_pos
            board.cat_pos = move
            eval = minimax(board, depth-1, True, alpha, beta)
            board.cat_pos = original_pos
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Configuración de Pygame
pygame.init()
font = pygame.font.SysFont(None, 36)
width, height = 400, 400
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Función principal del juego
def main():
    board = Board(5)  # Tamaño del tablero
    game_over = False
    start_time = time.time()
    time_limit = 30  # Tiempo límite en segundos

    while not game_over:
        screen.fill(WHITE)

        # Dibujar el tablero
        cell_size = min(width // board.size, height // board.size)
        for x in range(board.size):
            for y in range(board.size):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, BLACK, rect, 1)
                if (x, y) == board.cat_pos:
                    pygame.draw.circle(screen, RED, rect.center, cell_size // 4)
                elif (x, y) == board.mouse_pos:
                    pygame.draw.circle(screen, BLUE, rect.center, cell_size // 4)

        # Verificar si el gato atrapó al ratón
        if board.cat_pos == board.mouse_pos:
            game_over = True
            elapsed_time = time.time() - start_time
            if elapsed_time <= time_limit:
                text = font.render("¡El gato atrapó al ratón!", True, GREEN)
            else:
                text = font.render("¡Se acabó el tiempo!", True, RED)
            text_rect = text.get_rect(center=(width // 2, height // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(30)

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                game_over = True

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
