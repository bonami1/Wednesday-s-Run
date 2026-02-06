import random
import pygame
from Settings import OBSTACLE_BASE_SPEED, GROUND_Y


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, speed):
        super().__init__()
        self.type = type.lower()
        self.speed = speed

        # --- Animation (par défaut: aucune) ---
        self.frames = None
        self.frame_index = 0
        self.anim_delay = 120  # ms entre frames
        self.last_anim_time = pygame.time.get_ticks()

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
            # 🐦 Corbeau animé (2 frames)
            f1 = pygame.image.load("Assets/corbeau1.png").convert_alpha()
            f2 = pygame.image.load("Assets/corbeau2.png").convert_alpha()

            f1 = pygame.transform.scale(f1, (120, 140))
            f2 = pygame.transform.scale(f2, (120, 140))

            self.frames = [f1, f2]
            self.image = self.frames[0]
            self.rect = self.image.get_rect()

            self.rect.y = random.randint(15, 200)

            # --- comportement plongée ---
            self.diving = False
            self.dive_speed = random.randint(8, 12)
            self.dive_trigger_x = random.randint(400, 700)
            self.will_dive = random.random() < 0.5

        elif type == "chauve_souris":
            # 🦇 Chauve-souris animée (2 frames)
            f1 = pygame.image.load("Assets/bat1.png").convert_alpha()
            f2 = pygame.image.load("Assets/bat2.png").convert_alpha()

            f1 = pygame.transform.scale(f1, (80, 60))
            f2 = pygame.transform.scale(f2, (80, 60))

            self.frames = [f1, f2]
            self.image = self.frames[0]
            self.rect = self.image.get_rect()

            self.rect.y = GROUND_Y - 200

        else:
            self.image = pygame.Surface((120, 140), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.y = GROUND_Y - self.rect.height

        # Position de départ
        self.rect.x = 1000

        # ✅ Masque pixel-perfect
        threshold = 230 if self.type in ("corbeau", "chauve_souris") else 200
        self.mask = pygame.mask.from_surface(self.image, threshold)

    def animate(self):
        """Anime si des frames existent (corbeau / chauve-souris)."""
        if not self.frames:
            return

        now = pygame.time.get_ticks()
        if now - self.last_anim_time >= self.anim_delay:
            self.last_anim_time = now
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

            # Mise à jour du mask à chaque frame
            self.mask = pygame.mask.from_surface(self.image, 230)

    def update(self):
        # Animation d'abord
        self.animate()

        self.rect.x -= self.speed

        # --- COMPORTEMENT CORBEAU ---
        if self.type == "corbeau":
            if self.will_dive and not self.diving and self.rect.x < self.dive_trigger_x:
                self.diving = True

            if self.diving:
                self.rect.y += self.dive_speed
                max_y = GROUND_Y - self.rect.height
                if self.rect.y > max_y:
                    self.rect.y = max_y

        if self.rect.x < -150:
            self.kill()
