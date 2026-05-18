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

    def draw(self):
        # Sol
        pygame.draw.rect(self.screen, GREEN, self.ground)

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
