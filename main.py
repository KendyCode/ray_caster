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
        self.image = pygame.Surface((44, 44))

        # Sans ça, ton cercle rouge sera dans un carré noir ou blanc
        self.image.set_colorkey((0, 0, 0))

        # 3. On dessine le cercle au CENTRE de cette surface
        # Le centre est donc (50, 50) pour une surface de 100x100
        pygame.draw.circle(self.image, (255, 0, 0), (22, 22), 20)

        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self.angle = 0

        # On initialise les positions flottantes sur le coin du rect
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)

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
            self.pos_x += dx
            self.rect.x = int(self.pos_x) # On met à jour le rect pour le test de collision
            if pygame.sprite.spritecollide(self, world.walls, False, pygame.sprite.collide_mask):
                self.pos_x-= dx
            # On gère Y
            self.pos_y += dy
            self.rect.y = int(self.pos_y)
            if pygame.sprite.spritecollide(self, world.walls, False, pygame.sprite.collide_mask):
                self.pos_y -= dy

        # 4. Reculer
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            # On gère X (on fait l'inverse : - dx)
            self.pos_x -= dx
            self.rect.x = int(self.pos_x)
            if pygame.sprite.spritecollide(self, world.walls, False, pygame.sprite.collide_mask):
                self.pos_x += dx
            # On gère Y
            self.pos_y -= dy
            self.rect.y = int(self.pos_y)
            if pygame.sprite.spritecollide(self, world.walls, False, pygame.sprite.collide_mask):
                self.pos_y += dy

        # Très important : On synchronise le rect final
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

    def draw_direction(self, surface):
        angle_rad = math.radians(self.angle)
        line_x = self.rect.centerx + math.cos(angle_rad) * 50
        line_y = self.rect.centery + math.sin(angle_rad) * 50

        # On dessine sur la surface passée en argument (le screen)
        pygame.draw.line(surface, (0, 255, 0), self.rect.center, (line_x, line_y), 3)

    def cast_rays(self, surface):
        # On définit le début du cône (ex: l'angle actuel - 30 degrés)
        start_angle = self.angle - 30
        #
        for i in range(60): # On lance 60 rayons
            current_angle = start_angle + i

            # On commence au centre du joueur
            ray_x = self.rect.centerx
            ray_y = self.rect.centery

            # On prépare les petits pas du rayon
            angle_rad = math.radians(current_angle)

            # On avance de 1 pixel à chaque fois pour être précis
            dx = math.cos(angle_rad)
            dy = math.sin(angle_rad)

            # On fait avancer le rayon (limite à 1000 pixels pour éviter les boucles infinies)
            for depth in range(1000):

                ray_x += dx
                ray_y += dy
                # 1. On trouve la case correspondante
                col = int(ray_x // 100)
                row = int(ray_y // 100)
                index = row * 8 + col

                # 2. On vérifie qu'on est bien dans les limites de la map
                if 0 <= col < 8 and 0 <= row < 5: # Largeur 8, Hauteur 5
                    if map[index] == 1: # On utilise la liste 'map' globale
                        pygame.draw.line(surface, "Red", self.rect.center, (ray_x, ray_y), 1)
                        break
                else:
                    # Si le rayon sort de la map, on arrête de chercher
                    break













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

print(world.map_data)


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
    j1.cast_rays(screen)

    # Pour afficher la ligne de direction
    j1.draw_direction(screen)



    pygame.display.update()
    # MAX 60 image par seconde
    clock.tick(60)