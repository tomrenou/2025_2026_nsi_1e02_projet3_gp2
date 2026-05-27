import pygame

class Enemy:
    def __init__(self, x, y, min_x, max_x):
        self.image = pygame.image.load("enemy.png").convert_alpha()

        # Taille réduite
        self.image = pygame.transform.scale(self.image, (25, 25))

        # Hitbox = taille de l'image
        self.rect = self.image.get_rect(topleft=(x, y))

        self.rect.y += 23

        self.speed = 1
        self.direction = 1

        self.min_x = min_x
        self.max_x = max_x

    def update(self):
        self.rect.x += self.speed * self.direction

        if self.rect.x <= self.min_x:
            self.direction = 1
        elif self.rect.x >= self.max_x:
            self.direction = -1

    def draw(self, screen):
        screen.blit(self.image, self.rect)
