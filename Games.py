"""import pygame
import random
import os
from Parametres import *
from Mercredi import Player
from Obstacle import Obstacle


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mercredi Runner")
        self.clock = pygame.time.Clock()

        # ---------- BACKGROUNDS (MODIFIÉ) ----------
        # Liste des noms de tes fichiers (Mets tes vrais noms ici !)
        self.bg_filenames = [
            "Assets/background_clair.png",  # Image 1 (0 - 1999)
            "Assets/Background.png",   # Image 2 (2000 - 3999)
            "Assets/background_red.png"     # Image 3 (4000 - 5999) -> puis boucle
        ]
        
        self.bg_images = []
        for filename in self.bg_filenames:
            # On charge et on redimensionne chaque image
            try:
                img = pygame.image.load(filename).convert()
                img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.bg_images.append(img)
            except pygame.error as e:
                print(f"⚠️ Erreur chargement fond {filename}: {e}")
                # En cas d'erreur, on crée un fond noir par défaut pour éviter le crash
                surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                surf.fill((0, 0, 0))
                self.bg_images.append(surf)

        self.current_bg_index = 0
        
        # ---------- ETAT ----------
        # MENU / SCOREBOARD / PLAYING / PAUSED / GAME_OVER
        self.state = "MENU"

        # ---------- GROUPES ----------
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.player = None

        # ---------- JEU ----------
        self.score = 0
        self.timer = 0.0
        self.lives = 3
        self.spawn_timer = 0

        # ---------- BEST SCORE ----------
        self.best_score_file = "best_score.txt"
        self.best_score = self.load_best_score()

        # ---------- BOUTONS (MENU) ----------
        self.btn_play = pygame.Rect(SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 40, 280, 60)
        self.btn_scoreboard = pygame.Rect(SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 40, 280, 60)
        self.btn_quit = pygame.Rect(SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 120, 280, 60)

        # ---------- BOUTONS (SCOREBOARD) ----------
        self.btn_back = pygame.Rect(30, 30, 160, 50)

        # ---------- BOUTON REJOUER (GAME OVER) ----------
        self.replay_button = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 70, 240, 60)

        # ---------- BOUTON MENU (PAUSE + GAME OVER) ----------
        self.menu_button = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 140, 240, 60)

        # ---------- AUDIO ----------
        self.music_on = True
        self.volume = 50
        self.volume_animation = 0

        # musique
        try:
            pygame.mixer.music.load("Wednesdaybgm.mp3")
            pygame.mixer.music.set_volume(self.volume / 100)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print("⚠️ Musique non chargée:", e)

        # son game over
        try:
            self.game_over_sound = pygame.mixer.Sound("Assets/gameover.mp3")
            self.game_over_sound.set_volume(0.8)
        except pygame.error as e:
            print("⚠️ Son Game Over non chargé:", e)
            self.game_over_sound = None

        # polices
        self.font_big = pygame.font.SysFont("Arial", 72, bold=True)
        self.font_mid = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 24)

        # vitesse de course
        self.obstacle_speed = OBSTACLE_BASE_SPEED
        self.last_speed_step = 0

        # Lancé de la "main"
        self.projectiles = pygame.sprite.Group()

        self.hand_icon = pygame.image.load("Assets/Main.png").convert_alpha()
        self.hand_icon = pygame.transform.scale(self.hand_icon, (40, 40))
        self.hand_icon_gray = self.hand_icon.copy()
        self.hand_icon_gray.fill((100, 100, 100, 180), special_flags=pygame.BLEND_RGBA_MULT)

    # ================= BEST SCORE =================
    def load_best_score(self):
        if os.path.exists(self.best_score_file):
            try:
                with open(self.best_score_file, "r", encoding="utf-8") as f:
                    return int(f.read().strip() or 0)
            except:
                return 0
        return 0

    def save_best_score(self):
        try:
            with open(self.best_score_file, "w", encoding="utf-8") as f:
                f.write(str(self.best_score))
        except:
            pass

    def update_best_score_if_needed(self):
        if self.score > self.best_score:
            self.best_score = self.score
            self.save_best_score()

    # ================= AUDIO =================
    def change_volume(self, delta):
        self.volume = max(0, min(100, self.volume + delta))
        pygame.mixer.music.set_volume(self.volume / 100)
        self.volume_animation = 60

    def toggle_music(self):
        if self.music_on:
            pygame.mixer.music.pause()
            self.music_on = False
        else:
            pygame.mixer.music.unpause()
            self.music_on = True
        self.volume_animation = 60

    # ================= PAUSE =================
    def toggle_pause(self):
        if self.state == "PLAYING":
            self.state = "PAUSED"
            pygame.mixer.music.pause()
        elif self.state == "PAUSED":
            self.state = "PLAYING"
            pygame.mixer.music.unpause()

    # ================= MENU / START / RESET =================
    def go_to_menu(self):
        # reset partie
        self.all_sprites.empty()
        self.obstacles.empty()
        self.player = None

        self.score = 0
        self.timer = 0.0
        self.lives = 3
        self.spawn_timer = 0

        self.state = "MENU"

        # relancer la musique (si activée)
        if self.music_on:
            pygame.mixer.music.play(-1)

    def start_game(self):
        self.all_sprites.empty()
        self.obstacles.empty()

        self.player = Player()
        self.all_sprites.add(self.player)

        self.score = 0
        self.timer = 0.0
        self.lives = 3
        self.spawn_timer = 0

        self.state = "PLAYING"

        if self.music_on:
            pygame.mixer.music.play(-1)

        self.obstacle_speed = OBSTACLE_BASE_SPEED
        self.last_speed_step = 0

        # Lancé de la "main"
        self.projectiles.empty()

    def reset_game(self):
        self.start_game()

    # ================= OBSTACLES =================
    def spawn_obstacle(self):
        obstacle = Obstacle(random.choice(["wolf", "hyde", "corbeau", "chauve_souris"]),
                            self.obstacle_speed)
        self.obstacles.add(obstacle)
        self.all_sprites.add(obstacle)

    # ================= MAIN LOOP =================
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # touches globales (volume)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.toggle_music()
                    if event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                        self.change_volume(+5)
                    if event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        self.change_volume(-5)

                    # pause uniquement en jeu
                    if event.key == pygame.K_p and self.state in ("PLAYING", "PAUSED"):
                        self.toggle_pause()

                    # tirer la "main"
                    if event.key == pygame.K_SPACE:
                        if self.state == "PLAYING" and self.player.has_hand:
                            from Hand import HandProjectile
                            hand = HandProjectile(
                                self.player.rect.right,
                                self.player.rect.centery
                            )
                            self.projectiles.add(hand)
                            self.all_sprites.add(hand)
                            self.player.has_hand = False  # usage unique

                # clics souris
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos

                    if self.state == "MENU":
                        if self.btn_play.collidepoint(mx, my):
                            self.start_game()
                        elif self.btn_scoreboard.collidepoint(mx, my):
                            self.state = "SCOREBOARD"
                        elif self.btn_quit.collidepoint(mx, my):
                            running = False

                    elif self.state == "SCOREBOARD":
                        if self.btn_back.collidepoint(mx, my):
                            self.state = "MENU"

                    elif self.state == "PAUSED":
                        if self.menu_button.collidepoint(mx, my):
                            self.go_to_menu()

                    elif self.state == "GAME_OVER":
                        if self.replay_button.collidepoint(mx, my):
                            self.reset_game()
                        elif self.menu_button.collidepoint(mx, my):
                            self.go_to_menu()

            # ---------- LOGIQUE JEU ----------
            if self.state == "PLAYING":
                self.spawn_timer += 1
                if self.spawn_timer > 90:
                    self.spawn_obstacle()
                    self.spawn_timer = 0

                self.player.update(keys, dt)
                self.obstacles.update()
                self.projectiles.update()

                # ---- COLLISION MAIN / OBSTACLES ----
                pygame.sprite.groupcollide(
                    self.projectiles,
                    self.obstacles,
                    True,   # détruit la main
                    True,   # détruit l'obstacle
                    pygame.sprite.collide_mask
                )

                hits = pygame.sprite.spritecollide(
                    self.player, self.obstacles, True, pygame.sprite.collide_mask
                )
                if hits:
                    got_bonus = False
                    print("COLLISION AVEC :", [o.type for o in hits])

                    # donner la "main" au joueur
                    for obstacle in hits:
                        print("TYPE OBSTACLE =", obstacle.type)
                        if obstacle.type == "chauve_souris":
                            self.player.has_hand = True
                            got_bonus = True
                    # si ce n'est pas un bonus -> perdre une vie
                    if not got_bonus:
                        self.lives -= 1

                if self.lives <= 0:
                    self.lives = 0  # sécurité visuelle
                    self.update_best_score_if_needed()
                    self.state = "GAME_OVER"
                    pygame.mixer.music.stop()
                    if self.game_over_sound:
                        self.game_over_sound.play()

                self.score += 1

                # ---- CHANGEMENT DE BACKGROUND TOUS LES 2000 POINTS ----          
                if len(self.bg_images) > 0:
                    self.current_bg_index = (self.score // 2000) % len(self.bg_images)

                # ---- AUGMENTATION DE LA VITESSE TOUS LES 1000 POINTS ----
                current_step = self.score // SCORE_SPEED_STEP
                if current_step > self.last_speed_step:
                    self.last_speed_step = current_step
                    self.obstacle_speed += OBSTACLE_SPEED_INCREMENT

                self.timer += 1 / FPS

            self.draw()

        pygame.quit()

    # ================= DRAW HELPERS =================
    def draw_volume_ui(self):
        if self.volume_animation <= 0:
            return

        bar_w, bar_h = 200, 12
        x = SCREEN_WIDTH - bar_w - 20
        y = 20

        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, bar_w, bar_h))
        fill_w = int(bar_w * (self.volume / 100))
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, fill_w, bar_h))

        label = "MUTED" if not self.music_on else f"VOL {self.volume}%"
        txt = self.font_small.render(label, True, (255, 255, 255))
        self.screen.blit(txt, (x, y + 16))

        self.volume_animation -= 1

    def draw_hand_hud(self):
        x, y = 10, 170  # position HUD

        if not self.player:
            return

        if self.player.has_hand:
            # icône active
            self.screen.blit(self.hand_icon, (x, y))

            txt = self.font_small.render("SPACE", True, (255, 220, 220))
            self.screen.blit(txt, (x + 50, y + 10))
        else:
            # icône grisée
            self.screen.blit(self.hand_icon_gray, (x, y))

    def draw_button(self, rect, text, bg_color, text_color=(0, 0, 0)):
        pygame.draw.rect(self.screen, bg_color, rect, border_radius=14)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, width=3, border_radius=14)
        t = self.font_mid.render(text, True, text_color)
        self.screen.blit(t, (rect.centerx - t.get_width() // 2, rect.centery - t.get_height() // 2))

    # ================= SCREENS =================
    def draw_menu(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(90)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        violet = (180, 80, 255)
        title = self.font_big.render("MERCR. RUN", True, violet)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120))

        subtitle = self.font_small.render("Play • Scoreboard • Quit", True, (230, 230, 230))
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 210))

        self.draw_button(self.btn_play, "PLAY", violet)
        self.draw_button(self.btn_scoreboard, "SCOREBOARD", (255, 255, 255), (0, 0, 0))
        self.draw_button(self.btn_quit, "QUITTER", (255, 80, 80), (0, 0, 0))

        best = self.font_small.render(f"Meilleur score : {self.best_score}", True, (255, 255, 255))
        self.screen.blit(best, (SCREEN_WIDTH // 2 - best.get_width() // 2, SCREEN_HEIGHT - 60))

    def draw_scoreboard(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(140)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        violet = (180, 80, 255)
        title = self.font_big.render("SCOREBOARD", True, violet)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 140))

        best = self.font_mid.render(f"Meilleur score : {self.best_score}", True, (255, 255, 255))
        self.screen.blit(best, (SCREEN_WIDTH // 2 - best.get_width() // 2, 280))

        self.draw_button(self.btn_back, "RETOUR", (255, 255, 255))

    def draw_pause(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        violet = (180, 80, 255)
        text = self.font_big.render("PAUSE", True, violet)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 170))

        hint = self.font_small.render("Appuie sur P pour reprendre", True, (230, 230, 230))
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT // 2 - 70))

        self.draw_button(self.menu_button, "MENU", (255, 255, 255))

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        violet = (180, 80, 255)

        title = self.font_big.render("GAME OVER", True, violet)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 220))

        score_text = self.font_mid.render(f"Score final : {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 130))

        best_text = self.font_small.render(f"Meilleur score : {self.best_score}", True, (200, 200, 200))
        self.screen.blit(best_text, (SCREEN_WIDTH // 2 - best_text.get_width() // 2, SCREEN_HEIGHT // 2 - 85))

        self.draw_button(self.replay_button, "REJOUER", violet)
        self.draw_button(self.menu_button, "MENU", (255, 255, 255))

    # ================= DRAW FRAME =================
    def draw(self):
        if self.bg_images:
            self.screen.blit(self.bg_images[self.current_bg_index], (0, 0))
        else:
            self.screen.fill((0,0,0)) # Fallback si pas d'images

        if self.state in ("PLAYING", "PAUSED", "GAME_OVER"):
            pygame.draw.line(self.screen, (0, 0, 0), (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 3)
            self.all_sprites.draw(self.screen)

            hud_score = self.font_small.render(f"Score: {self.score}", True, (255, 255, 255))
            hud_lives = self.font_small.render(f"Vies: {self.lives}", True, (255, 255, 255))
            self.screen.blit(hud_score, (10, 110))
            self.screen.blit(hud_lives, (10, 140))

            self.draw_hand_hud()

        self.draw_volume_ui()

        if self.state == "MENU":
            self.draw_menu()
        elif self.state == "SCOREBOARD":
            self.draw_scoreboard()
        elif self.state == "PAUSED":
            self.draw_pause()
        elif self.state == "GAME_OVER":
            self.draw_game_over()

        pygame.display.flip()
"""



import pygame
import random
import os
from Parametres import *
from Mercredi import Player
from Obstacle import Obstacle


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mercredi Runner")
        self.clock = pygame.time.Clock()

        # ---------- BACKGROUNDS (MODIFIÉ) ----------
        # Liste des noms de tes fichiers (Mets tes vrais noms ici !)
        self.bg_filenames = [
            "Assets/background_clair.png",  # Image 1 (0 - 1999)
            "Assets/Background.png",   # Image 2 (2000 - 3999)
            "Assets/background_red.png"     # Image 3 (4000 - 5999) -> puis boucle
        ]
        
        self.bg_images = []
        for filename in self.bg_filenames:
            # On charge et on redimensionne chaque image
            try:
                img = pygame.image.load(filename).convert()
                img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.bg_images.append(img)
            except pygame.error as e:
                print(f"⚠️ Erreur chargement fond {filename}: {e}")
                # En cas d'erreur, on crée un fond noir par défaut pour éviter le crash
                surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                surf.fill((0, 0, 0))
                self.bg_images.append(surf)

        self.current_bg_index = 0
        
        # ---------- ETAT ----------
        # MENU / SCOREBOARD / PLAYING / PAUSED / GAME_OVER
        self.state = "MENU"

        # ---------- GROUPES ----------
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.player = None

        # ---------- JEU ----------
        self.score = 0
        self.timer = 0.0
        self.lives = 3
        self.spawn_timer = 0

        # ---------- BEST SCORE ----------
        self.best_score_file = "best_score.txt"
        self.best_score = self.load_best_score()

        # ---------- BOUTONS (MENU) ----------
        self.btn_play = pygame.Rect(SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 40, 280, 60)
        self.btn_scoreboard = pygame.Rect(SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 40, 280, 60)
        self.btn_quit = pygame.Rect(SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 120, 280, 60)

        # ---------- BOUTONS (SCOREBOARD) ----------
        self.btn_back = pygame.Rect(30, 30, 160, 50)

        # ---------- BOUTON REJOUER (GAME OVER) ----------
        self.replay_button = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 70, 240, 60)

        # ---------- BOUTON MENU (PAUSE + GAME OVER) ----------
        self.menu_button = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 140, 240, 60)

        # ---------- AUDIO ----------
        self.music_on = True
        self.volume = 50
        self.volume_animation = 0

        # musique
        try:
            pygame.mixer.music.load("Wednesdaybgm.mp3")
            pygame.mixer.music.set_volume(self.volume / 100)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print("⚠️ Musique non chargée:", e)

        # son game over
        try:
            self.game_over_sound = pygame.mixer.Sound("Assets/gameover.mp3")
            self.game_over_sound.set_volume(0.8)
        except pygame.error as e:
            print("⚠️ Son Game Over non chargé:", e)
            self.game_over_sound = None

        # --- NOUVEAU : SON IMPACT / BLESSURE ---
        try:
            # Assure-toi d'avoir un fichier 'hit.wav' dans Assets
            self.hit_sound = pygame.mixer.Sound("Assets/hit.mp3")
            self.hit_sound.set_volume(0.6)
        except pygame.error as e:
            print("⚠️ Son Hit non chargé (vérifie le nom du fichier):", e)
            self.hit_sound = None

        # polices
        self.font_big = pygame.font.SysFont("Arial", 72, bold=True)
        self.font_mid = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 24)

        # vitesse de course
        self.obstacle_speed = OBSTACLE_BASE_SPEED
        self.last_speed_step = 0

        # Lancé de la "main"
        self.projectiles = pygame.sprite.Group()

        self.hand_icon = pygame.image.load("Assets/Main.png").convert_alpha()
        self.hand_icon = pygame.transform.scale(self.hand_icon, (40, 40))
        self.hand_icon_gray = self.hand_icon.copy()
        self.hand_icon_gray.fill((100, 100, 100, 180), special_flags=pygame.BLEND_RGBA_MULT)

    # ================= BEST SCORE =================
    def load_best_score(self):
        if os.path.exists(self.best_score_file):
            try:
                with open(self.best_score_file, "r", encoding="utf-8") as f:
                    return int(f.read().strip() or 0)
            except:
                return 0
        return 0

    def save_best_score(self):
        try:
            with open(self.best_score_file, "w", encoding="utf-8") as f:
                f.write(str(self.best_score))
        except:
            pass

    def update_best_score_if_needed(self):
        if self.score > self.best_score:
            self.best_score = self.score
            self.save_best_score()

    # ================= AUDIO =================
    def change_volume(self, delta):
        self.volume = max(0, min(100, self.volume + delta))
        pygame.mixer.music.set_volume(self.volume / 100)
        self.volume_animation = 60

    def toggle_music(self):
        if self.music_on:
            pygame.mixer.music.pause()
            self.music_on = False
        else:
            pygame.mixer.music.unpause()
            self.music_on = True
        self.volume_animation = 60

    # ================= PAUSE =================
    def toggle_pause(self):
        if self.state == "PLAYING":
            self.state = "PAUSED"
            pygame.mixer.music.pause()
        elif self.state == "PAUSED":
            self.state = "PLAYING"
            pygame.mixer.music.unpause()

    # ================= MENU / START / RESET =================
    def go_to_menu(self):
        # reset partie
        self.all_sprites.empty()
        self.obstacles.empty()
        self.player = None

        self.score = 0
        self.timer = 0.0
        self.lives = 3
        self.spawn_timer = 0

        self.state = "MENU"

        # relancer la musique (si activée)
        if self.music_on:
            pygame.mixer.music.play(-1)

    def start_game(self):
        self.all_sprites.empty()
        self.obstacles.empty()

        self.player = Player()
        self.all_sprites.add(self.player)

        self.score = 0
        self.timer = 0.0
        self.lives = 3
        self.spawn_timer = 0

        self.state = "PLAYING"

        if self.music_on:
            pygame.mixer.music.play(-1)

        self.obstacle_speed = OBSTACLE_BASE_SPEED
        self.last_speed_step = 0

        # Lancé de la "main"
        self.projectiles.empty()

    def reset_game(self):
        self.start_game()

    # ================= OBSTACLES =================
    def spawn_obstacle(self):
        obstacle = Obstacle(random.choice(["wolf", "hyde", "corbeau", "chauve_souris"]),
                            self.obstacle_speed)
        self.obstacles.add(obstacle)
        self.all_sprites.add(obstacle)

    # ================= MAIN LOOP =================
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # touches globales (volume)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.toggle_music()
                    if event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                        self.change_volume(+5)
                    if event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        self.change_volume(-5)

                    # pause uniquement en jeu
                    if event.key == pygame.K_p and self.state in ("PLAYING", "PAUSED"):
                        self.toggle_pause()

                    # tirer la "main"
                    if event.key == pygame.K_SPACE:
                        if self.state == "PLAYING" and self.player.has_hand:
                            from Hand import HandProjectile
                            hand = HandProjectile(
                                self.player.rect.right,
                                self.player.rect.centery
                            )
                            self.projectiles.add(hand)
                            self.all_sprites.add(hand)
                            self.player.has_hand = False  # usage unique

                # clics souris
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos

                    if self.state == "MENU":
                        if self.btn_play.collidepoint(mx, my):
                            self.start_game()
                        elif self.btn_scoreboard.collidepoint(mx, my):
                            self.state = "SCOREBOARD"
                        elif self.btn_quit.collidepoint(mx, my):
                            running = False

                    elif self.state == "SCOREBOARD":
                        if self.btn_back.collidepoint(mx, my):
                            self.state = "MENU"

                    elif self.state == "PAUSED":
                        if self.menu_button.collidepoint(mx, my):
                            self.go_to_menu()

                    elif self.state == "GAME_OVER":
                        if self.replay_button.collidepoint(mx, my):
                            self.reset_game()
                        elif self.menu_button.collidepoint(mx, my):
                            self.go_to_menu()

            # ---------- LOGIQUE JEU ----------
            if self.state == "PLAYING":
                self.spawn_timer += 1
                if self.spawn_timer > 90:
                    self.spawn_obstacle()
                    self.spawn_timer = 0

                self.player.update(keys, dt)
                self.obstacles.update()
                self.projectiles.update()

                # ---- COLLISION MAIN / OBSTACLES ----
                pygame.sprite.groupcollide(
                    self.projectiles,
                    self.obstacles,
                    True,   # détruit la main
                    True,   # détruit l'obstacle
                    pygame.sprite.collide_mask
                )

                hits = pygame.sprite.spritecollide(
                    self.player, self.obstacles, True, pygame.sprite.collide_mask
                )
                if hits:
                    got_bonus = False
                    print("COLLISION AVEC :", [o.type for o in hits])

                    # donner la "main" au joueur
                    for obstacle in hits:
                        print("TYPE OBSTACLE =", obstacle.type)
                        if obstacle.type == "chauve_souris":
                            self.player.has_hand = True
                            got_bonus = True
                    
                    # si ce n'est pas un bonus -> perdre une vie
                    if not got_bonus:
                        # --- MODIFICATION ICI : JOUER LE SON ---
                        if self.hit_sound:
                            self.hit_sound.play()
                        
                        self.lives -= 1

                if self.lives <= 0:
                    self.lives = 0  # sécurité visuelle
                    self.update_best_score_if_needed()
                    self.state = "GAME_OVER"
                    pygame.mixer.music.stop()
                    if self.game_over_sound:
                        self.game_over_sound.play()

                self.score += 1

                # ---- CHANGEMENT DE BACKGROUND TOUS LES 2000 POINTS ----          
                if len(self.bg_images) > 0:
                    self.current_bg_index = (self.score // 2000) % len(self.bg_images)

                # ---- AUGMENTATION DE LA VITESSE TOUS LES 1000 POINTS ----
                current_step = self.score // SCORE_SPEED_STEP
                if current_step > self.last_speed_step:
                    self.last_speed_step = current_step
                    self.obstacle_speed += OBSTACLE_SPEED_INCREMENT

                self.timer += 1 / FPS

            self.draw()

        pygame.quit()

    # ================= DRAW HELPERS =================
    def draw_volume_ui(self):
        if self.volume_animation <= 0:
            return

        bar_w, bar_h = 200, 12
        x = SCREEN_WIDTH - bar_w - 20
        y = 20

        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, bar_w, bar_h))
        fill_w = int(bar_w * (self.volume / 100))
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, fill_w, bar_h))

        label = "MUTED" if not self.music_on else f"VOL {self.volume}%"
        txt = self.font_small.render(label, True, (255, 255, 255))
        self.screen.blit(txt, (x, y + 16))

        self.volume_animation -= 1

    def draw_hand_hud(self):
        x, y = 10, 170  # position HUD

        if not self.player:
            return

        if self.player.has_hand:
            # icône active
            self.screen.blit(self.hand_icon, (x, y))

            txt = self.font_small.render("SPACE", True, (255, 220, 220))
            self.screen.blit(txt, (x + 50, y + 10))
        else:
            # icône grisée
            self.screen.blit(self.hand_icon_gray, (x, y))

    def draw_button(self, rect, text, bg_color, text_color=(0, 0, 0)):
        pygame.draw.rect(self.screen, bg_color, rect, border_radius=14)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, width=3, border_radius=14)
        t = self.font_mid.render(text, True, text_color)
        self.screen.blit(t, (rect.centerx - t.get_width() // 2, rect.centery - t.get_height() // 2))

    # ================= SCREENS =================
    def draw_menu(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(90)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        violet = (180, 80, 255)
        title = self.font_big.render("MERCR. RUN", True, violet)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120))

        subtitle = self.font_small.render("Play • Scoreboard • Quit", True, (230, 230, 230))
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 210))

        self.draw_button(self.btn_play, "PLAY", violet)
        self.draw_button(self.btn_scoreboard, "SCOREBOARD", (255, 255, 255), (0, 0, 0))
        self.draw_button(self.btn_quit, "QUITTER", (255, 80, 80), (0, 0, 0))

        best = self.font_small.render(f"Meilleur score : {self.best_score}", True, (255, 255, 255))
        self.screen.blit(best, (SCREEN_WIDTH // 2 - best.get_width() // 2, SCREEN_HEIGHT - 60))

    def draw_scoreboard(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(140)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        violet = (180, 80, 255)
        title = self.font_big.render("SCOREBOARD", True, violet)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 140))

        best = self.font_mid.render(f"Meilleur score : {self.best_score}", True, (255, 255, 255))
        self.screen.blit(best, (SCREEN_WIDTH // 2 - best.get_width() // 2, 280))

        self.draw_button(self.btn_back, "RETOUR", (255, 255, 255))

    def draw_pause(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        violet = (180, 80, 255)
        text = self.font_big.render("PAUSE", True, violet)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 170))

        hint = self.font_small.render("Appuie sur P pour reprendre", True, (230, 230, 230))
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT // 2 - 70))

        self.draw_button(self.menu_button, "MENU", (255, 255, 255))

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        violet = (180, 80, 255)

        title = self.font_big.render("GAME OVER", True, violet)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 220))

        score_text = self.font_mid.render(f"Score final : {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 130))

        best_text = self.font_small.render(f"Meilleur score : {self.best_score}", True, (200, 200, 200))
        self.screen.blit(best_text, (SCREEN_WIDTH // 2 - best_text.get_width() // 2, SCREEN_HEIGHT // 2 - 85))

        self.draw_button(self.replay_button, "REJOUER", violet)
        self.draw_button(self.menu_button, "MENU", (255, 255, 255))

    # ================= DRAW FRAME =================
    def draw(self):
        if self.bg_images:
            self.screen.blit(self.bg_images[self.current_bg_index], (0, 0))
        else:
            self.screen.fill((0,0,0)) # Fallback si pas d'images

        if self.state in ("PLAYING", "PAUSED", "GAME_OVER"):
            pygame.draw.line(self.screen, (0, 0, 0), (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 3)
            self.all_sprites.draw(self.screen)

            hud_score = self.font_small.render(f"Score: {self.score}", True, (255, 255, 255))
            hud_lives = self.font_small.render(f"Vies: {self.lives}", True, (255, 255, 255))
            self.screen.blit(hud_score, (10, 110))
            self.screen.blit(hud_lives, (10, 140))

            self.draw_hand_hud()

        self.draw_volume_ui()

        if self.state == "MENU":
            self.draw_menu()
        elif self.state == "SCOREBOARD":
            self.draw_scoreboard()
        elif self.state == "PAUSED":
            self.draw_pause()
        elif self.state == "GAME_OVER":
            self.draw_game_over()

        pygame.display.flip()