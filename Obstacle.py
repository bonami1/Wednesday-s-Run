import pygame
from Parametres import OBSTACLE_BASE_SPEED, GROUND_Y

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, speed):
        super().__init__()
        self.type = type.lower()
        self.speed = speed 

        # --- Charger l'image selon le type ---
        if type == "wolf":
            self.image = pygame.image.load("Assets/Loup_garou.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 80))
            self.rect = self.image.get_rect()
            self.rect.y = GROUND_Y - self.rect.height

        elif type == "hyde":
            self.image = pygame.image.load("Assets/Hyde.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 80))
            self.rect = self.image.get_rect()
            self.rect.y = GROUND_Y - self.rect.height

        elif type == "corbeau":
            self.image = pygame.image.load("Assets/Corbeau.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 80))
            self.rect = self.image.get_rect()
            self.rect.y = GROUND_Y - 150

        elif type == "chauve_souris":
            self.image = pygame.image.load("Assets/Chauve_souris.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 80))
            self.rect = self.image.get_rect()
            self.rect.y = GROUND_Y - 200

        else:
            # sécurité si type inconnu
            self.image = pygame.Surface((60, 80), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.y = GROUND_Y - self.rect.height

        # Position de départ
        self.rect.x = 1000

        # ✅ Masque (pixel-perfect) : basé sur les pixels non transparents
        self.mask = pygame.mask.from_surface(self.image, 200)

    def update(self):
        self.rect.x -= OBSTACLE_BASE_SPEED
        if self.rect.x < -100:
            self.kill()
