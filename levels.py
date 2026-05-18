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
            pygame.Rect(200, 420, 20, 20),
            pygame.Rect(500, 320, 20, 20),
            pygame.Rect(180, 220, 20, 20)
        ]

        self.weapon = pygame.Rect(700, 500, 30, 30)

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
            pygame.Rect(350, 520, 40, 30),
            pygame.Rect(600, 520, 40, 30),
            pygame.Rect(250, 430, 30, 20)
        ]

        # Joueur
        self.player = Player(100, 470)

        # ENNEMIS (nouveau)
        self.enemies = [
            Enemy(0, 490, 0, 300),        # Ennemi qui patrouille à gauche
            Enemy(500, 490, 500, 750)     # Ennemi qui patrouille à droite
        ]

    def update(self):
        # Mise à jour du joueur
        self.player.update(self.ground, self.platforms, self.obstacles)

        # Mise à jour des ennemis
        for enemy in self.enemies:
            enemy.update()

        # Collision joueur / ennemi
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                print("Le joueur a été touché !")
                # Reset position du joueur
                self.player.rect.topleft = (100, 470)

        self.player.update(self.ground, self.platforms, self.obstacles)

        # ramassage pièces
        for coin in self.coins[:]:
            if self.player.rect.colliderect(coin):
                self.coins.remove(coin)
                self.player.score += 10

        # ramassage arme
        if self.weapon and self.player.rect.colliderect(self.weapon):
            self.player.has_weapon = True
            self.weapon = None

    def draw(self):
        # Sol
        pygame.draw.rect(self.screen, GREEN, self.ground)
        for i in range(self.player.lives):
            self.screen.blit(self.heart, (10 + i * 45, 10))
        
        # Plateformes
        for p in self.platforms:
            pygame.draw.rect(self.screen, GREY, p)

        # Obstacles
        for o in self.obstacles:
            pygame.draw.rect(self.screen, RED, o)

        # ENNEMIS
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Joueur
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

