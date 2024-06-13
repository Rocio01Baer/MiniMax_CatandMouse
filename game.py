import pygame
import sys
import time
import random
from pygame.locals import *

# Importar la clase Board desde otro archivo
from board import Board

class Game:
    def __init__(self, board_size):
        # Inicialización del juego
        self.board = Board(board_size)  # Crear un tablero
        self.board_size = board_size
        self.cell_size = 80  # Tamaño de cada celda del tablero
        self.screen_size = (self.cell_size * board_size, self.cell_size * board_size)  # Tamaño de la ventana
        self.screen = pygame.display.set_mode(self.screen_size)  # Crear la ventana del juego
        self.clock = pygame.time.Clock()  # Crear un reloj para controlar el tiempo
        self.mouse_image = pygame.image.load("mouse.png").convert_alpha()  # Cargar la imagen del ratón
        self.mouse_image = pygame.transform.scale(self.mouse_image, (self.cell_size, self.cell_size))  # Escalar la imagen
        self.cat_image = pygame.image.load("cat.png").convert_alpha()  # Cargar la imagen del gato
        self.cat_image = pygame.transform.scale(self.cat_image, (self.cell_size, self.cell_size))  # Escalar la imagen

    # Método para iniciar el juego
    def play(self, chase_time):
        start_time = time.time()  # Tiempo de inicio del juego
        while time.time() - start_time < chase_time:  # Mientras no haya pasado el tiempo límite
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
            self.clock.tick(30)  # Controlar los FPS

            # Actualizar posiciones del ratón y el gato (movimiento aleatorio)
            self.board.mouse_pos = self.random_move(self.board.mouse_pos)
            self.board.cat_pos = self.random_move(self.board.cat_pos)

            # Manejo de eventos
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

    # Método para moverse aleatoriamente en el tablero
    def random_move(self, position):
        x, y = position
        dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Movimiento aleatorio
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < self.board_size and 0 <= new_y < self.board_size:
            return new_x, new_y
        return x, y

if __name__ == "__main__":
    pygame.init()  # Inicializar Pygame

    # Solicitar al usuario el tamaño del tablero y el tiempo de persecución
    board_size = int(input("Ingrese el tamaño del tablero: "))
    chase_time = float(input("Ingrese el tiempo de persecución (en segundos): "))

    game = Game(board_size)  # Crear una instancia del juego
    game.play(chase_time)  # Iniciar el juego con el tiempo de persecución proporcionado
