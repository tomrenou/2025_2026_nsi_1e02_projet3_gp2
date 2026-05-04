import pygame

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

        # Obstacles (ex: blocs rouges)
        self.obstacles = [
            pygame.Rect(350, 520, 40, 30),
            pygame.Rect(600, 520, 40, 30),
            pygame.Rect(250, 430, 30, 20)
        ]

    def draw(self):
        # Sol
        pygame.draw.rect(self.screen, GREEN, self.ground)

        # Plateformes
        for p in self.platforms:
            pygame.draw.rect(self.screen, GREY, p)

        # Obstacles
        for o in self.obstacles:
            pygame.draw.rect(self.screen, RED, o)

    def update(self):
        #ajouter du gameplay ici (collisions, ennemis, etc.)
        pass
