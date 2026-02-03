import pygame
import random
from Parametres import OBSTACLE_SPEED, GROUND_Y

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type

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

        self.rect.x = 1000

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.x < -100:
            self.kill()
