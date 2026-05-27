import pygame

class Enemy:
    def __init__(self, x, y, min_x, max_x):
        self.image_right = pygame.image.load("enemy.png").convert_alpha()
        self.image_right = pygame.transform.scale(self.image_right, (25, 25))
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right

        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.y += 23

        self.speed = 1
        self.direction = 1

        self.min_x = min_x
        self.max_x = max_x

        # IA agressive
        self.aggressive = False
        self.kill_count = 0
        self.chase_speed = 1.5

        # Pause après avoir touché le joueur
        self.gloat_timer = 0

    def on_hit_player(self):
        """Appelé depuis levels.py quand cet ennemi touche le joueur."""
        self.aggressive = True
        self.gloat_timer = 30  # pause 0.5 sec
        self.kill_count = min(self.kill_count + 1, 4)  # plafonné à 4
        self.chase_speed = min(1.5 + self.kill_count * 0.5, 5)

    def update(self, player=None):

        # Pause satisfaction après avoir touché
        if self.gloat_timer > 0:
            self.gloat_timer -= 1
            return

        if self.aggressive and player is not None:
            # Fonce vers le joueur
            if player.rect.centerx < self.rect.centerx:
                self.rect.x -= self.chase_speed
                self.image = self.image_left
                self.direction = -1
            else:
                self.rect.x += self.chase_speed
                self.image = self.image_right
                self.direction = 1

        else:
            # Patrouille normale
            self.rect.x += self.speed * self.direction

            if self.direction == 1:
                self.image = self.image_right
            else:
                self.image = self.image_left

            if self.rect.x <= self.min_x:
                self.direction = 1
            elif self.rect.x >= self.max_x:
                self.direction = -1

    def draw(self, screen):
        screen.blit(self.image, self.rect)
