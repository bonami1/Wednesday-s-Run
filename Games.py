import pygame
import random
from Parametres import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GROUND_Y
from Mercredi import Player
from Obstacle import Obstacle

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mercredi Runner")
        self.clock = pygame.time.Clock()

        self.bg = pygame.image.load("Assets/Background.png").convert()
        self.bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.player = Player()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.obstacles = pygame.sprite.Group()

        self.score = 0
        self.timer = 0
        self.lives = 3

        self.spawn_timer = 0

        self.paused = False


    def spawn_obstacle(self):
        types = ["wolf", "hyde", "corbeau", "chauve_souris"]
        obstacle_type = random.choice(types)
        obstacle = Obstacle(obstacle_type)
        self.obstacles.add(obstacle)
        self.all_sprites.add(obstacle)

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.toggle_pause()

            keys = pygame.key.get_pressed()

            if not self.paused:
                self.player.update(keys)
                self.spawn_timer += 1
                if self.spawn_timer > 90:
                    self.spawn_obstacle()
                    self.spawn_timer = 0

                self.obstacles.update()


                # Collision
                hits = pygame.sprite.spritecollide(self.player, self.obstacles, True)
                if hits:
                    self.lives -= 1
                    if self.lives <= 0:
                        running = False

                self.score += 1
                self.timer += 1 / FPS

            self.draw()

        self.game_over()

    def draw(self):
        pygame.draw.line(self.screen, (255,0,0), (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 3)

        self.screen.blit(self.bg, (0, 0))
        pygame.draw.line(self.screen, (0,0,0), (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 3)

        self.all_sprites.draw(self.screen)

        font = pygame.font.SysFont("Arial", 24)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        timer_text = font.render(f"Temps: {int(self.timer)}s", True, (255, 255, 255))
        lives_text = font.render(f"Vies: {self.lives}", True, (255, 255, 255))

        self.screen.blit(score_text, (10, 110))
        self.screen.blit(timer_text, (10, 140))
        self.screen.blit(lives_text, (10, 170))

        if self.paused:
            font = pygame.font.SysFont("Arial", 60)
            pause_text = font.render("PAUSE", True, (255, 255, 0))
            self.screen.blit(
                pause_text,
                (SCREEN_WIDTH // 2 - pause_text.get_width() // 2,
                SCREEN_HEIGHT // 2 - pause_text.get_height() // 2)
            )
        
        pygame.display.flip()


    def toggle_pause(self):
        self.paused = not self.paused


    def game_over(self):
        font = pygame.font.SysFont("Arial", 48)
        text = font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
