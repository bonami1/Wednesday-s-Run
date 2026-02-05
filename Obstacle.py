import random
import pygame
from Settings import OBSTACLE_BASE_SPEED, GROUND_Y

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, speed):
        super().__init__()
        self.type = type.lower()
        self.speed = speed 

        # --- Charger l'image selon le type ---
        if type == "wolf":
            self.image = pygame.image.load("Assets/Loup_garou.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (120, 140))
            self.rect = self.image.get_rect()
            self.rect.y = GROUND_Y - self.rect.height

        elif type == "hyde":
            self.image = pygame.image.load("Assets/Hyde.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (120, 140))
            self.rect = self.image.get_rect()
            self.rect.y = GROUND_Y - self.rect.height

        elif type == "corbeau":
            self.image = pygame.image.load("Assets/Corbeau.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (120, 140))
            self.rect = self.image.get_rect()

            # Commence haut dans le ciel
            self.rect.y = random.randint(15, 200)

            # --- comportement plongée ---
            self.diving = False
            self.dive_speed = random.randint(8, 12)
            self.dive_trigger_x = random.randint(400, 700)

            # plongée aléatoire
            self.will_dive = random.random() < 0.5   # 50% de chance

        elif type == "chauve_souris":
            self.image = pygame.image.load("Assets/Chauve_souris.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (120, 140))
            self.rect = self.image.get_rect()
            self.rect.y = GROUND_Y - 200

        else:
            # sécurité si type inconnu
            self.image = pygame.Surface((120, 140), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.y = GROUND_Y - self.rect.height

        # Position de départ
        self.rect.x = 1000

        # ✅ Masque (pixel-perfect) : basé sur les pixels non transparents
        self.mask = pygame.mask.from_surface(self.image, 200)

    def update(self):
        self.rect.x -= self.speed

        # --- COMPORTEMENT CORBEAU ---
        if self.type == "corbeau":
            # Déclenche la plongée quand il s'approche du joueur
            if self.will_dive and not self.diving and self.rect.x < self.dive_trigger_x:
                self.diving = True

            if self.diving:
                self.rect.y += self.dive_speed

                # Limite basse (ne traverse pas le sol)
                max_y = GROUND_Y - self.rect.height
                if self.rect.y > max_y:
                    self.rect.y = max_y

        if self.rect.x < -150:
            self.kill()