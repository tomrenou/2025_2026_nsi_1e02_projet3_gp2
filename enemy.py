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

        # IA : timer en frames (2 min = 7200 frames à 60fps)
        self.ai_timer = 0          # incrémenté à chaque update
        self.ai_active = False     # devient True après 2 min
        self.chase_speed = 1       # vitesse de poursuite (augmente avec le temps)

    def update(self, player=None):

        self.ai_timer += 1

        # Activation IA après 2 minutes
        if self.ai_timer >= 7200:
            self.ai_active = True

        if self.ai_active and player is not None:

            # Vitesse de poursuite qui augmente progressivement
            # toutes les 30 secondes (1800 frames) après activation
            frames_since_activation = self.ai_timer - 7200
            self.chase_speed = 1 + (frames_since_activation // 1800) * 0.5
            self.chase_speed = min(self.chase_speed, 4)  # max vitesse = 4

            # Se diriger vers le joueur
            if player.rect.centerx < self.rect.centerx:
                self.rect.x -= self.chase_speed
                self.direction = -1
                self.image = self.image_left
            else:
                self.rect.x += self.chase_speed
                self.direction = 1
                self.image = self.image_right

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