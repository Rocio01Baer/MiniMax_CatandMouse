import pygame
import sys
import time
import random
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

class Game:
    def __init__(self, board_size, max_moves):
        # Inicialización del juego
        self.board = Board(board_size)  # Crear un tablero
        self.board_size = board_size
        self.max_moves = max_moves  # Máximo de movimientos permitidos
        self.cell_size = 80  # Tamaño de cada celda del tablero
        self.screen_size = (self.cell_size * board_size, self.cell_size * board_size)  # Tamaño de la ventana
        self.screen = pygame.display.set_mode(self.screen_size)  # Crear la ventana del juego
        self.clock = pygame.time.Clock()  # Crear un reloj para controlar el tiempo
        self.mouse_image = pygame.image.load("mouse.png").convert_alpha()  # Cargar la imagen del ratón
        self.mouse_image = pygame.transform.scale(self.mouse_image, (self.cell_size, self.cell_size))  # Escalar la imagen
        self.cat_image = pygame.image.load("cat.png").convert_alpha()  # Cargar la imagen del gato
        self.cat_image = pygame.transform.scale(self.cat_image, (self.cell_size, self.cell_size))  # Escalar la imagen

    # Método para iniciar el juego
    def play(self):
        moves = 0  # Contador de movimientos

        while moves < self.max_moves:  # Mientras no haya pasado el tiempo límite y haya movimientos restantes
            self.screen.fill((255, 255, 255))  # Llenar la pantalla de blanco

            # Dibujar el tablero
            for x in range(self.board_size):
                for y in range(self.board_size):
                    rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

            # Dibujar el ratón
            mouse_rect = self.mouse_image.get_rect(topleft=(self.board.mouse_pos[0] * self.cell_size, self.board.mouse_pos[1] * self.cell_size))
            self.screen.blit(self.mouse_image, mouse_rect)

            # Dibujar el gato
            cat_rect = self.cat_image.get_rect(topleft=(self.board.cat_pos[0] * self.cell_size, self.board.cat_pos[1] * self.cell_size))
            self.screen.blit(self.cat_image, cat_rect)

            pygame.display.flip()  # Actualizar la pantalla

            # Agregar un retraso entre movimientos
            time.sleep(0.5)  # Retraso de 0.5 segundos

            # Movimiento del ratón usando una combinación de Minimax y movimiento aleatorio
            if random.random() < 0.8:  # 80% de probabilidad de usar Minimax
                best_move = None
                best_value = float('-inf')
                for move in get_neighbors(self.board.mouse_pos, self.board.size):
                    original_pos = self.board.mouse_pos
                    self.board.mouse_pos = move
                    move_value = minimax(self.board, 3, False, float('-inf'), float('inf'))
                    self.board.mouse_pos = original_pos
                    if move_value > best_value:
                        best_value = move_value
                        best_move = move
                self.board.mouse_pos = best_move
            else:  # 20% de probabilidad de moverse aleatoriamente
                self.board.mouse_pos = random.choice(get_neighbors(self.board.mouse_pos, self.board.size))

            # Movimiento del gato usando una combinación de Minimax y movimiento aleatorio
            if random.random() < 0.8:  # 80% de probabilidad de usar Minimax
                best_move = None
                best_value = float('inf')
                for move in get_neighbors(self.board.cat_pos, self.board.size):
                    original_pos = self.board.cat_pos
                    self.board.cat_pos = move
                    move_value = minimax(self.board, 3, True, float('-inf'), float('inf'))
                    self.board.cat_pos = original_pos
                    if move_value < best_value:
                        best_value = move_value
                        best_move = move
                self.board.cat_pos = best_move
            else:  # 20% de probabilidad de moverse aleatoriamente
                self.board.cat_pos = random.choice(get_neighbors(self.board.cat_pos, self.board.size))

            # Comprobar si el gato ha atrapado al ratón
            if self.board.cat_pos == self.board.mouse_pos:
                print("¡El gato atrapó al ratón! El gato gana.")
                return

            moves += 1  # Incrementar el contador de movimientos

            # Manejo de eventos
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

        # Si el juego termina sin que el gato atrape al ratón
        print("¡El ratón escapó! El ratón gana.")

if __name__ == "__main__":
    pygame.init()  # Inicializar Pygame

    # Solicitar al usuario el tamaño del tablero y el número máximo de movimientos
    board_size = int(input("Ingrese el tamaño del tablero: "))
    max_moves = int(input("Ingrese el número máximo de movimientos: "))

    game = Game(board_size, max_moves)  # Crear una instancia del juego con el número máximo de movimientos
    game.play()  # Iniciar el juego
