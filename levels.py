import pygame
from player import Player
from enemy import Enemy

WHITE = (255, 255, 255)
SKY = (120, 190, 255)
GRASS = (60, 180, 75)
DIRT = (110, 75, 40)
PLATFORM = (90, 90, 110)
SPIKE = (200, 50, 50)
YELLOW = (255, 215, 0)

# Position initiale des pièces
COINS_INITIAL = [
    pygame.Rect(150, 420, 20, 20),
    pygame.Rect(500, 320, 20, 20),
    pygame.Rect(180, 220, 20, 20)
]

class Level1:
    def __init__(self, screen, image_path="Liorbleu.png"):
        self.screen = screen
        self.image_path = image_path
        self.heart = pygame.image.load("heart.png").convert_alpha()
        self.heart = pygame.transform.scale(self.heart, (40, 40))

        # Fond
        self.background_color = SKY

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
            pygame.Rect(90, 430, 190, 22),
            pygame.Rect(330, 340, 240, 22),
            pygame.Rect(140, 240, 180, 22)
        ]

        # Obstacles (piques)
        self.obstacles = [
            pygame.Rect(430, 520, 40, 30),
            pygame.Rect(600, 520, 40, 30),
            pygame.Rect(250, 430, 30, 20)
        ]

        # Joueur
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

        # Fond bleu ciel
        self.screen.fill(self.background_color)

        # Sol : bande herbe + bande terre
        pygame.draw.rect(self.screen, GRASS, pygame.Rect(0, 550, 800, 15))
        pygame.draw.rect(self.screen, DIRT, pygame.Rect(0, 565, 800, 35))

        # Plateformes
        for p in self.platforms:
            pygame.draw.rect(self.screen, PLATFORM, p)
            # Petite bande herbe sur le dessus
            pygame.draw.rect(self.screen, GRASS, pygame.Rect(p.x, p.y, p.w, 5))

        # Obstacles (piques)
        for o in self.obstacles:
            pygame.draw.rect(self.screen, SPIKE, o)

        # Pièces
        for coin in self.coins:
            pygame.draw.circle(self.screen, YELLOW, coin.center, 10)

        # Compte à rebours réapparition pièces
        if len(self.coins) == 0 and self.coin_respawn_timer > 0:
            font = pygame.font.SysFont(None, 28)
            secs = self.coin_respawn_timer // 60 + 1
            txt = font.render(f"Pièces dans {secs}s", True, YELLOW)
            self.screen.blit(txt, (340, 10))

        # Arme
        if self.weapon:
            pygame.draw.rect(self.screen, (0, 0, 255), self.weapon)

        # Ennemis
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Joueur
        self.player.draw(self.screen)

        # HUD — vies
        for i in range(self.player.lives):
            self.screen.blit(self.heart, (10 + i * 45, 10))

        # HUD — score et arme
        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f"Score: {self.player.score}", True, (20, 20, 30))
        self.screen.blit(score_text, (650, 10))

        weapon_text = font.render(
            f"Arme: {'Oui' if self.player.has_weapon else 'Non'}",
            True, (20, 20, 30)
        )
        self.screen.blit(weapon_text, (620, 45))

        # HUD — munitions
        self.player.draw_hud(self.screen)

        # Écran Game Over
        if self.state == "GAME_OVER":
            overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))

            font_big = pygame.font.SysFont(None, 90)
            font_med = pygame.font.SysFont(None, 55)

            title    = font_big.render("GAME OVER", True, (255, 0, 0))
            restart  = font_med.render("R  —  Recommencer", True, (255, 255, 255))
            quit_txt = font_med.render("Echap  —  Quitter", True, (255, 255, 255))

            self.screen.blit(title,    ((800 - title.get_width()) // 2, 180))
            self.screen.blit(restart,  ((800 - restart.get_width()) // 2, 310))
            self.screen.blit(quit_txt, ((800 - quit_txt.get_width()) // 2, 380))