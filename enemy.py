import pygame

class Enemy:
    def __init__(self, x, y, min_x, max_x):
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))

        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed = 2
        self.direction = 1  # 1 = droite, -1 = gauche

        # Limites de patrouille
        self.min_x = min_x
        self.max_x = max_x

    def update(self):
        # Déplacement horizontal
        self.rect.x += self.speed * self.direction

        # Si on atteint une limite → demi-tour
        if self.rect.x <= self.min_x:
            self.direction = 1
        elif self.rect.x >= self.max_x:
            self.direction = -1

    def draw(self, screen):
        screen.blit(self.image, self.rect)
