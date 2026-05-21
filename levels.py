import pygame
from player import Player
from enemy import Enemy   # ← AJOUT

WHITE = (255, 255, 255)
GREY = (120, 120, 120)
GREEN = (50, 200, 50)
RED = (200, 50, 50)

class Level1:
    def __init__(self, screen):
        self.screen = screen
        self.heart = pygame.image.load("heart.png").convert_alpha()
        self.heart = pygame.transform.scale(self.heart, (40, 40))

        self.coins = [
            pygame.Rect(150, 420, 20, 20),
            pygame.Rect(500, 320, 20, 20),
            pygame.Rect(180, 220, 20, 20)
        ]
        
        # armes
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

        # Joueur
        self.player = Player(180, 190)

        # ENNEMIS (nouveau)
        self.enemies = [
            Enemy(0, 490, 0, 300),        # Ennemi qui patrouille à gauche
            Enemy(500, 490, 500, 750)     # Ennemi qui patrouille à droite
        ]
        self.enemy_respawn_timer = 0

        # Game over
        self.game_over = False
        self.state = "PLAY"

    def update(self):
        self.player.update(self.ground, self.platforms, self.obstacles)
        
        # game over
        for enemy in self.enemies:
            enemy.update()
        if self.state != "PLAY":
            return
        
        # Collision joueur / ennemi
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect) and not self.player.invincible:
                self.player.lives -= 1
                self.player.rect.topleft = (180, 190)
                self.player.invincible = True
                self.player.invincible_timer = 60
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.colliderect(enemy.rect):
                    self.player.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.player.score += 50
                    break
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

        # ramassage pièces
        for coin in self.coins[:]:
            if self.player.rect.colliderect(coin):
                self.coins.remove(coin)
                self.player.score += 10

        # ramassage arme
        if self.weapon and self.player.rect.colliderect(self.weapon):
            self.player.has_weapon = True
            self.weapon = None
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # game over
        if self.game_over:
            return
        if self.player.lives <= 0:
            self.game_over = True
        if self.player.lives <= 0:
            self.state = "GAME_OVER"

    def draw(self):
        pygame.draw.rect(self.screen, GREEN, self.ground)

        for i in range(self.player.lives):
            self.screen.blit(self.heart, (10 + i * 45, 10))

        for p in self.platforms:
            pygame.draw.rect(self.screen, GREY, p)

        for o in self.obstacles:
            pygame.draw.rect(self.screen, RED, o)

        # Pièces
        for coin in self.coins:
            pygame.draw.circle(self.screen, (255, 215, 0), coin.center, 10)

        # Arme
        if self.weapon:
            pygame.draw.rect(self.screen, (0, 0, 255), self.weapon)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.player.draw(self.screen)

        font = pygame.font.SysFont(None, 35)

        score_text = font.render(f"Score: {self.player.score}", True, WHITE)
        self.screen.blit(score_text, (650, 10))

        weapon_text = font.render(
            f"Arme: {'Oui' if self.player.has_weapon else 'Non'}",
            True,
            WHITE
        )
        self.screen.blit(weapon_text, (620, 45))

        # game over
        if self.game_over:
            font = pygame.font.SysFont(None, 80)
            text = font.render("GAME OVER", True, (255, 0, 0))
            self.screen.blit(text, (250, 250))
            return
        if self.state == "GAME_OVER":
            font = pygame.font.SysFont(None, 60)

            title = font.render("GAME OVER", True, (255, 0, 0))
            restart = font.render("R - Restart", True, (255, 255, 255))
            menu = font.render("M - Menu", True, (255, 255, 255))
            quit_text = font.render("Q - Quitter", True, (255, 255, 255))

            self.screen.blit(title, (260, 150))
            self.screen.blit(restart, (280, 300))
            self.screen.blit(menu, (300, 360))
            self.screen.blit(quit_text, (280, 420))
            return