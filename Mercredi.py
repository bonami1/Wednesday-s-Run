import pygame
from Parametres import GROUND_Y, GRAVITY, JUMP_VELOCITY, DUCK_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.size = (80, 100)

        # --------- LOAD RUN (5 frames) ----------
        self.run_frames = [
            pygame.image.load("Assets/Run/run1.png").convert_alpha(),
            pygame.image.load("Assets/Run/run2.png").convert_alpha(),
            pygame.image.load("Assets/Run/run3.png").convert_alpha(),
            pygame.image.load("Assets/Run/run4.png").convert_alpha(),
            pygame.image.load("Assets/Run/run5.png").convert_alpha(),
        ]
        self.run_frames = [pygame.transform.scale(img, self.size) for img in self.run_frames]

        # --------- LOAD JUMP (5 frames) ----------
        # Ordre: 1 départ / 2-3 montée / 4 descente / 5 fin
        self.jump_frames = [
            pygame.image.load("Assets/Jump/jump1.png").convert_alpha(),
            pygame.image.load("Assets/Jump/jump2.png").convert_alpha(),
            pygame.image.load("Assets/Jump/jump3.png").convert_alpha(),
            pygame.image.load("Assets/Jump/jump4.png").convert_alpha(),
            pygame.image.load("Assets/Jump/jump5.png").convert_alpha(),
        ]
        self.jump_frames = [pygame.transform.scale(img, self.size) for img in self.jump_frames]

        # Image initiale
        self.image = self.run_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = 80
        self.rect.y = GROUND_Y - self.rect.height

        # ✅ Masque initial (pixel-perfect)
        self.mask = pygame.mask.from_surface(self.image)

        # Physique / état
        self.vel_y = 0
        self.jumping = False
        self.ducking = False

        # Run animation
        self.run_index = 0
        self.anim_timer = 0
        self.ANIM_SPEED = 100  # ms par frame

        # posseder la "main"
        self.has_hand = False

    def start_jump(self):
        self.jumping = True
        self.vel_y = JUMP_VELOCITY

    def handle_input(self, keys):
        # Jump
        if keys[pygame.K_UP] and not self.jumping and not self.ducking:
            self.start_jump()

        # Duck
        if keys[pygame.K_DOWN] and not self.jumping:
            self.ducking = True
        else:
            self.ducking = False

    def apply_physics(self):
        if self.jumping:
            self.vel_y += GRAVITY
            self.rect.y += self.vel_y

            # Toucher le sol
            ground_target = GROUND_Y - self.rect.height
            if self.rect.y >= ground_target:
                self.rect.y = ground_target
                self.jumping = False
                self.vel_y = 0

        # Position duck
        if self.ducking:
            self.rect.y = GROUND_Y - DUCK_HEIGHT
        else:
            if not self.jumping:
                self.rect.y = GROUND_Y - self.rect.height

    def set_image(self, new_image):
        """Change l'image et met à jour le mask automatiquement (indispensable pour collide_mask)."""
        if self.image is not new_image:
            self.image = new_image
            self.mask = pygame.mask.from_surface(self.image)

    def update_animation(self, dt):
        # ---- JUMP animation (5 frames) basée sur vel_y ----
        if self.jumping:
            if self.vel_y < -6:
                idx = 0
            elif self.vel_y < -2:
                idx = 1
            elif -2 <= self.vel_y <= 2:
                idx = 2
            elif self.vel_y <= 6:
                idx = 3
            else:
                idx = 4

            self.set_image(self.jump_frames[idx])
            return

        # ---- DUCK (sans frames dédiées pour l’instant) ----
        if self.ducking:
            self.set_image(self.run_frames[0])
            return

        # ---- RUN animation (boucle 5 frames) ----
        self.anim_timer += dt
        if self.anim_timer >= self.ANIM_SPEED:
            self.anim_timer = 0
            self.run_index = (self.run_index + 1) % len(self.run_frames)

        self.set_image(self.run_frames[self.run_index])

    def update(self, keys, dt):
        self.handle_input(keys)
        self.apply_physics()
        self.update_animation(dt)
