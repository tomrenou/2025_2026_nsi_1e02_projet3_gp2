import pygame
from player import Player
from enemy import Enemy

WHITE = (255, 255, 255)
GREY = (120, 120, 120)
GREEN = (50, 200, 50)
RED = (200, 50, 50)
YELLOW = (255, 215, 0)

# Position initiale des pièces
COINS_INITIAL = [
    pygame.Rect(150, 420, 20, 20),
    pygame.Rect(500, 320, 20, 20),
    pygame.Rect(180, 220, 20, 20)
]

class Level1:
    def __init__(self, screen, image_path="Liorbleu.png"):  # ← image_path ajouté
        self.screen = screen
        self.image_path = image_path  # ← on le garde pour le reset
        self.heart = pygame.image.load("heart.png").convert_alpha()
        self.heart = pygame.transform.scale(self.heart, (40, 40))

        # Pièces
        self.coins = [pygame.Rect(c.x, c.y, c.w, c.h) for c in COINS_INITIAL]
        self.coin_respawn_timer = 0

        # Arme
        self.weapon = pygame.Rect(700, 500, 30, 30)
        self.shoot_cooldown = 0

        # Sol
        self.ground = pygame.Rect(0, 550, 800, 50)

        # Plateformes
        self.platforms = [
            pygame.Rect(100, 450, 200, 20),
            pygame.Rect(400, 350, 250, 20),
            pygame.Rect(150, 250, 180, 20)
        ]

        # Obstacles
        self.obstacles = [
            pygame.Rect(430, 520, 40, 30),
            pygame.Rect(600, 520, 40, 30),
            pygame.Rect(250, 430, 30, 20)
        ]

        # Joueur — on passe l'image du personnage choisi
        self.player = Player(180, 190, image_path=image_path)

        # Ennemis
        self.enemies = [
            Enemy(0, 490, 0, 300),
            Enemy(500, 490, 500, 750)
        ]
        self.enemy_respawn_timer = 0

        # État du jeu
        self.state = "PLAY"

    def reset(self):
        self.__init__(self.screen, self.image_path)

    def update(self):

        if self.state == "GAME_OVER":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.reset()
                return
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                exit()
            return

        self.player.update(self.ground, self.platforms, self.obstacles)

        for enemy in self.enemies:
            enemy.update()

        # Collision joueur / ennemi
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect) and not self.player.invincible:
                self.player.lives -= 1
                self.player.rect.topleft = (180, 190)
                self.player.invincible = True
                self.player.invincible_timer = 60

        # Collision balles / ennemis
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet["rect"].colliderect(enemy.rect):
                    self.player.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.player.score += 50
                    break

        # Respawn ennemis
        if len(self.enemies) == 0:
            if self.enemy_respawn_timer == 0:
                self.enemy_respawn_timer = 300
            else:
                self.enemy_respawn_timer -= 1
                if self.enemy_respawn_timer <= 0:
                    self.enemies = [
                        Enemy(0, 490, 0, 300),
                        Enemy(500, 490, 500, 750)
                    ]
                    self.enemy_respawn_timer = 0

        # Ramassage pièces
        for coin in self.coins[:]:
            if self.player.rect.colliderect(coin):
                self.coins.remove(coin)
                self.player.score += 10

        # Réapparition pièces après 10 secondes
        if len(self.coins) == 0:
            if self.coin_respawn_timer == 0:
                self.coin_respawn_timer = 600
            else:
                self.coin_respawn_timer -= 1
                if self.coin_respawn_timer <= 0:
                    self.coins = [pygame.Rect(c.x, c.y, c.w, c.h) for c in COINS_INITIAL]
                    self.coin_respawn_timer = 0

        # Ramassage arme
        if self.weapon and self.player.rect.colliderect(self.weapon):
            self.player.has_weapon = True
            self.weapon = None

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # Game over
        if self.player.lives <= 0:
            self.state = "GAME_OVER"

    def draw(self):

        pygame.draw.rect(self.screen, GREEN, self.ground)
        for p in self.platforms:
            pygame.draw.rect(self.screen, GREY, p)

        for o in self.obstacles:
            pygame.draw.rect(self.screen, RED, o)

        for coin in self.coins:
            pygame.draw.circle(self.screen, YELLOW, coin.center, 10)

        if len(self.coins) == 0 and self.coin_respawn_timer > 0:
            font = pygame.font.SysFont(None, 28)
            secs = self.coin_respawn_timer // 60 + 1
            txt = font.render(f"Pièces dans {secs}s", True, YELLOW)
            self.screen.blit(txt, (340, 10))

        if self.weapon:
            pygame.draw.rect(self.screen, (0, 0, 255), self.weapon)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.player.draw(self.screen)

        for i in range(self.player.lives):
            self.screen.blit(self.heart, (10 + i * 45, 10))

        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f"Score: {self.player.score}", True, WHITE)
        self.screen.blit(score_text, (650, 10))

        weapon_text = font.render(
            f"Arme: {'Oui' if self.player.has_weapon else 'Non'}",
            True, WHITE
        )
        self.screen.blit(weapon_text, (620, 45))

        self.player.draw_hud(self.screen)

        if self.state == "GAME_OVER":
            overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))

            font_big = pygame.font.SysFont(None, 90)
            font_med = pygame.font.SysFont(None, 55)

            title    = font_big.render("GAME OVER", True, (255, 0, 0))
            restart  = font_med.render("R  —  Recommencer", True, WHITE)
            quit_txt = font_med.render("Echap  —  Quitter", True, WHITE)

            self.screen.blit(title,    ((800 - title.get_width()) // 2, 180))
            self.screen.blit(restart,  ((800 - restart.get_width()) // 2, 310))
            self.screen.blit(quit_txt, ((800 - quit_txt.get_width()) // 2, 380))