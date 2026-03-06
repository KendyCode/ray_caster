from random import shuffle

import pygame
import math
import random

map = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 1],
    [ 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1,],
    [1, 1, 1, 1, 1, 1, 1, 1]

]


TILE_SIZE = 100
MAP_HEIGHT = len(map)
MAP_WIDTH = len(map[0])
print(MAP_HEIGHT)
print(MAP_WIDTH)
WIDTH_2D = MAP_WIDTH * TILE_SIZE

class Tile(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        # Si on oublie de mettre super().__init__() on aura une erreur
        super().__init__()

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)


        # Le rectangle qui gère la position
        self.rect = self.image.get_rect(topleft=(x, y))

        self.mask = pygame.mask.from_surface(self.image)





class World:
    def __init__(self, game_map):
        super().__init__()
        self.map_data = game_map
        self.walls = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.generate_world()

    def generate_world(self):
        # On parcourt chaque ligne (y)
        for row_index, row in enumerate(self.map_data):
            # On parcourt chaque colonne (x) dans cette ligne
            for col_index, cell in enumerate(row):
                x_pos = col_index * TILE_SIZE
                y_pos = row_index * TILE_SIZE

                if cell == 1:
                    wall = Tile(x_pos, y_pos, (0, 0, 255))
                    self.walls.add(wall)
                    self.all_sprites.add(wall)


pygame.init()
screen = pygame.display.set_mode((MAP_WIDTH*100,MAP_HEIGHT*100))
pygame.display.set_caption("RayCaster")
world = World(map)

clock = pygame.time.Clock()

while True:
    # 1. Calcul du temps écoulé (en secondes)
    # On récupère le temps mais on dit  "Il ne peut pas dépasser 0.1 seconde"
    # Même si l'ordi freeze pendant 3 secondes, le jeu ne fera pas un bond énorme.
    dt = min(clock.tick(60) / 1000, 0.1)
    for event in pygame.event.get():
        #Pour fermer la fenetre
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    world.all_sprites.update() # Cela appellera automatiquement le update de TOUS les sprites
    # Color Background
    screen.fill((255, 255, 255))
    # On dessine tous les sprites du groupe en une seule ligne
    world.all_sprites.draw(screen)
    pygame.display.update()
