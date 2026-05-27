import pygame
from player import Player
from enemy import Enemy

WHITE = (255, 255, 255)
SKY = (120, 190, 255)
GRASS = (60, 180, 75)
DIRT = (110, 75, 40)
PLATFORM = (90, 90, 110)
SPIKE = (200, 50, 50)

class Level1:

    def __init__(self, screen, image_path="Liorbleu.png"):

        self.screen = screen

        # Fond
        self.background_color = SKY

        # Coeurs
        self.heart = pygame.image.load("heart.png").convert_alpha()
        self.heart = pygame.transform.scale(self.heart, (38, 38))

        # Joueur
        self.player = Player(180, 190, image_path)

        # Sol
        self.ground = pygame.Rect(0, 540, 800, 60)

        # Plateformes
        self.platforms = [
            pygame.Rect(90, 430, 190, 22),
            pygame.Rect(390, 340, 240, 22),
            pygame.Rect(140, 240, 180, 22)
        ]

        # Pics
        self.obstacles = [
            pygame.Rect(430, 510, 40, 30),
            pygame.Rect(600, 510, 40, 30),
            pygame.Rect(250, 400, 30, 30)
        ]

        # Pièces
        self.coins = [
            pygame.Rect(150, 390, 20, 20),
            pygame.Rect(500, 290, 20, 20),
            pygame.Rect(190, 190, 20, 20)
        ]

        # Arme
        self.weapon = pygame.Rect(700, 495, 32, 32)

        # Ennemis
        self.enemies = [
            Enemy(0, 490, 0, 300),
            Enemy(500, 490, 500, 750)
        ]

        self.enemy_respawn_timer = 0

        # État jeu
        self.game_over = False
        self.state = "PLAY"

    def update(self):

        self.player.update(
            self.ground,
            self.platforms,
            self.obstacles
        )

        # Ennemis
        for enemy in self.enemies:
            enemy.update()

        if self.state != "PLAY":
            return

        # Collision ennemis
        for enemy in self.enemies:

            if (
                self.player.rect.colliderect(enemy.rect)
                and not self.player.invincible
            ):

                self.player.lives -= 1
                self.player.rect.topleft = (180, 190)

                self.player.invincible = True
                self.player.invincible_timer = 60

        # Balles / ennemis
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

        # Game over
        if self.player.lives <= 0:

            self.game_over = True
            self.state = "GAME_OVER"

    def draw(self):

        # Fond ciel
        self.screen.fill(self.background_color)

        # Soleil
        pygame.draw.circle(
            self.screen,
            (255, 220, 80),
            (700, 90),
            50
        )

        # Nuages
        pygame.draw.circle(self.screen, WHITE, (130, 90), 30)
        pygame.draw.circle(self.screen, WHITE, (165, 90), 40)
        pygame.draw.circle(self.screen, WHITE, (205, 90), 30)

        pygame.draw.circle(self.screen, WHITE, (500, 140), 25)
        pygame.draw.circle(self.screen, WHITE, (530, 140), 35)
        pygame.draw.circle(self.screen, WHITE, (565, 140), 25)

        # Sol terre
        pygame.draw.rect(
            self.screen,
            DIRT,
            self.ground
        )

        # Herbe
        pygame.draw.rect(
            self.screen,
            GRASS,
            (0, 540, 800, 12)
        )

        # Plateformes
        for platform in self.platforms:

            pygame.draw.rect(
                self.screen,
                PLATFORM,
                platform,
                border_radius=8
            )

            pygame.draw.rect(
                self.screen,
                (140, 140, 170),
                platform,
                3,
                border_radius=8
            )

        # Pics
        for obstacle in self.obstacles:

            x = obstacle.x
            y = obstacle.y

            pygame.draw.polygon(
                self.screen,
                SPIKE,
                [
                    (x, y + 30),
                    (x + 15, y),
                    (x + 30, y + 30)
                ]
            )

        # Pièces
        for coin in self.coins:

            pygame.draw.circle(
                self.screen,
                (255, 215, 0),
                coin.center,
                11
            )

            pygame.draw.circle(
                self.screen,
                (255, 240, 120),
                coin.center,
                6
            )

        # Arme
        if self.weapon:

            pygame.draw.rect(
                self.screen,
                (40, 40, 40),
                self.weapon,
                border_radius=5
            )

            pygame.draw.rect(
                self.screen,
                (0, 120, 255),
                (self.weapon.x + 12, self.weapon.y - 10, 8, 15),
                border_radius=3
            )

        # Ennemis
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Joueur
        self.player.draw(self.screen)

        # Coeurs uniquement
        for i in range(self.player.lives):
            self.screen.blit(self.heart, (10 + i * 45, 10))

        # Score stylé
        font = pygame.font.SysFont("arialblack", 28)

        score_text = font.render(
            f"{self.player.score}",
            True,
            WHITE
        )

        self.screen.blit(score_text, (730, 10))

        # GAME OVER
        if self.state == "GAME_OVER":

            overlay = pygame.Surface((800, 600))
            overlay.set_alpha(170)
            overlay.fill((0, 0, 0))

            self.screen.blit(overlay, (0, 0))

            font_big = pygame.font.SysFont("arialblack", 80)
            font_med = pygame.font.SysFont("arialblack", 40)

            title = font_big.render(
                "GAME OVER",
                True,
                (255, 60, 60)
            )

            restart = font_med.render(
                "R - Restart",
                True,
                WHITE
            )

            quit_text = font_med.render(
                "Q - Quitter",
                True,
                WHITE
            )

            self.screen.blit(title, (170, 180))
            self.screen.blit(restart, (260, 320))
            self.screen.blit(quit_text, (255, 390))