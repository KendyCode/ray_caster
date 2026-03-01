import pygame
import math

map = [1, 1, 1, 1, 1, 1, 1, 1,
       1, 0, 0, 0, 1, 0, 0, 1,
       1, 0, 1, 0, 0, 1, 0, 1,
       1, 0, 0, 0, 0, 0, 0, 1,
       1, 1, 1, 1, 1, 1, 1, 1]

class Tile(pygame.sprite.Sprite):
    def __init__(self,x,y,color,is_wall=False):
        # Si on oublie de mettre super().__init__() on aura une erreur
        super().__init__()

        self.image = pygame.Surface((100, 100))
        self.image.fill(color)

        # Ajout du contour directement sur l'image du sprite
        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, 100, 100], 1)

        # Le rectangle qui gère la position
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_wall = is_wall # Pratique pour les futures collisions

        self.mask = pygame.mask.from_surface(self.image)



class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        # Si on oublie de mettre super().__init__() on aura une erreur
        super().__init__()

        # 1. On crée la surface (le "cadre" du sprite)
        self.image = pygame.Surface((100, 100))

        # Sans ça, ton cercle rouge sera dans un carré noir ou blanc
        self.image.set_colorkey((0, 0, 0))

        # 3. On dessine le cercle au CENTRE de cette surface
        # Le centre est donc (50, 50) pour une surface de 100x100
        pygame.draw.circle(self.image, (255, 0, 0), (50, 50), 20)

        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self.angle = 0

    def player_input(self):
        keys = pygame.key.get_pressed()

        # 1. Rotation
        if keys[pygame.K_q] or keys[pygame.K_LEFT]: self.angle -= 5
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.angle += 5

        # 2. Calcul du vecteur de mouvement (vitesse de 5 pixels)
        angle_rad = math.radians(self.angle)
        dx = math.cos(angle_rad) * 5
        dy = math.sin(angle_rad) * 5

        # 3. Avancer (Z ou UP)
        if keys[pygame.K_z] or keys[pygame.K_UP]:
            # On gère X
            self.rect.x += dx
            if pygame.sprite.spritecollide(self, world.walls, False, pygame.sprite.collide_mask):
                self.rect.x -= dx
            # On gère Y
            self.rect.y += dy
            if pygame.sprite.spritecollide(self, world.walls, False, pygame.sprite.collide_mask):
                self.rect.y -= dy

        # 4. Reculer
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            # On gère X (on fait l'inverse : - dx)
            self.rect.x -= dx
            if pygame.sprite.spritecollide(self, world.walls, False, pygame.sprite.collide_mask):
                self.rect.x += dx
            # On gère Y
            self.rect.y -= dy
            if pygame.sprite.spritecollide(self, world.walls, False, pygame.sprite.collide_mask):
                self.rect.y += dy

    def draw_direction(self, surface):
        angle_rad = math.radians(self.angle)
        line_x = self.rect.centerx + math.cos(angle_rad) * 50
        line_y = self.rect.centery + math.sin(angle_rad) * 50

        # On dessine sur la surface passée en argument (le screen)
        pygame.draw.line(surface, (0, 255, 0), self.rect.center, (line_x, line_y), 3)





    def update(self):
        self.player_input()


class World:
    def __init__(self, game_map):
        super().__init__()
        self.map_data = game_map
        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.generate_world()

    def generate_world(self):
        x_pos = 0
        y_pos = 0
        
        for i in self.map_data:
            if i == 1:
                # On crée un obstacle bleu et on l'ajoute au groupe
                wall = Tile(x_pos, y_pos, (0, 0, 255), is_wall=True)
                self.walls.add(wall)
                self.all_sprites.add(wall)
        
            else:
                floor = Tile(x_pos, y_pos, "Yellow", is_wall=False)
                self.floors.add(floor)
                self.all_sprites.add(floor)
        
            x_pos += 100
            if x_pos >= 800:
                x_pos = 0
                y_pos += 100










pygame.init()
screen = pygame.display.set_mode((1400,800))
pygame.display.set_caption("RayCaster")
clock = pygame.time.Clock()

world = World(map)
j1 = Player(150, 150, "Red")
world.all_sprites.add(j1)


while True:
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

    # Pour afficher la ligne de direction
    j1.draw_direction(screen)



    pygame.display.update()
    # MAX 60 image par seconde
    clock.tick(60)