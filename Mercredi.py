import pygame
from Parametres import GROUND_Y, GRAVITY, JUMP_VELOCITY, DUCK_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Assets/Wednesday.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 100))
        self.rect = self.image.get_rect()
        self.rect.x = 80
        self.rect.y = GROUND_Y - self.rect.height

        self.vel_y = 0
        self.jumping = False
        self.ducking = False

    def update(self, keys):
        if keys[pygame.K_UP] and not self.jumping and not self.ducking:
            self.jumping = True
            self.vel_y = JUMP_VELOCITY

        if keys[pygame.K_DOWN] and not self.jumping:
            self.ducking = True
        else:
            self.ducking = False

        if self.jumping:
            self.vel_y += GRAVITY
            self.rect.y += self.vel_y

            if self.rect.y >= GROUND_Y - self.rect.height:
                self.rect.y = GROUND_Y - self.rect.height
                self.jumping = False
                self.vel_y = 0

        if self.ducking:
            self.rect.y = GROUND_Y - DUCK_HEIGHT
        else:
            if not self.jumping:
                self.rect.y = GROUND_Y - self.rect.height
