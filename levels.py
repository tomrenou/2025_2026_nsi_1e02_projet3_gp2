import pygame
from player import Player
from enemy import Enemy

WHITE = (255, 255, 255)
GREY = (120, 120, 120)
GREEN = (50, 200, 50)
RED = (200, 50, 50)

class Level1:

    def __init__(self, screen, image_path="Liorbleu.png"):

        self.screen = screen
        # Coeur
        self.heart = pygame.image.load("heart.png").convert_alpha()
        self.heart = pygame.transform.scale(self.heart, (40, 40))
        # Pièces
        self.coins = [
            pygame.Rect(150, 420, 20, 20),
            pygame.Rect(500, 320, 20, 20),
            pygame.Rect(180, 220, 20, 20)
        ]
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

        # Joueur
        self.player = Player(180, 190, image_path)

        # Ennemis
        self.enemies = [
            Enemy(0, 490, 0, 300),
            Enemy(500, 490, 500, 750)
        ]

        self.enemy_respawn_timer = 0

        # État du jeu
        self.game_over = False
        self.state = "PLAY"

    def update(self):

        self.player.update(
            self.ground,
            self.platforms,
            self.obstacles
        )

        # Update ennemis
        for enemy in self.enemies:
            enemy.update()

        if self.state != "PLAY":
            return

        # Collision joueur / ennemi
        for enemy in self.enemies:

            if (
                self.player.rect.colliderect(enemy.rect)
                and not self.player.invincible
            ):

                self.player.lives -= 1
                self.player.rect.topleft = (180, 190)

                self.player.invincible = True
                self.player.invincible_timer = 60

        # Collision balles / ennemis
        for bullet in self.player.bullets[:]:

            for enemy in self.enemies[:]:

                if bullet.colliderect(enemy.rect):

                    if bullet in self.player.bullets:
                        self.player.bullets.remove(bullet)

                    if enemy in self.enemies:
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

        # Pièces
        for coin in self.coins[:]:

            if self.player.rect.colliderect(coin):

                self.coins.remove(coin)
                self.player.score += 10

        # Arme
        if self.weapon and self.player.rect.colliderect(self.weapon):

            self.player.has_weapon = True
            self.weapon = None

        # Cooldown tir
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # Game over
        if self.player.lives <= 0:

            self.game_over = True
            self.state = "GAME_OVER"

    def draw(self):

        # Sol
        pygame.draw.rect(self.screen, GREEN, self.ground)

        # Plateformes
        for platform in self.platforms:
            pygame.draw.rect(self.screen, GREY, platform)

        # Obstacles
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, RED, obstacle)

        # Pièces
        for coin in self.coins:
            pygame.draw.circle(
                self.screen,
                (255, 215, 0),
                coin.center,
                10
            )

        # Arme
        if self.weapon:
            pygame.draw.rect(
                self.screen,
                (0, 0, 255),
                self.weapon
            )

        # Ennemis
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Joueur
        self.player.draw(self.screen)

        # HUD vies
        for i in range(self.player.lives):
            self.screen.blit(self.heart, (10 + i * 45, 10))

        # HUD score / arme
        font = pygame.font.SysFont(None, 35)

        score_text = font.render(
            f"Score : {self.player.score}",
            True,
            WHITE
        )

        self.screen.blit(score_text, (620, 10))

        weapon_text = font.render(
            f"Arme : {'Oui' if self.player.has_weapon else 'Non'}",
            True,
            WHITE
        )

        self.screen.blit(weapon_text, (580, 45))

        # HUD player
        self.player.draw_hud(self.screen)

        # GAME OVER
        if self.state == "GAME_OVER":

            font_big = pygame.font.SysFont(None, 80)
            font_med = pygame.font.SysFont(None, 60)

            title = font_big.render(
                "GAME OVER",
                True,
                (255, 0, 0)
            )

            restart = font_med.render(
                "R - Restart",
                True,
                WHITE
            )

            menu = font_med.render(
                "M - Menu",
                True,
                WHITE
            )

            quit_text = font_med.render(
                "Q - Quitter",
                True,
                WHITE
            )
            self.screen.blit(title, (200, 150))
            self.screen.blit(restart, (260, 300))
            self.screen.blit(menu, (290, 360))
            self.screen.blit(quit_text, (250, 420))