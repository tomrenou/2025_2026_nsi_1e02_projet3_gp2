import pygame

WHITE = (255, 255, 255)

class Player:
    def __init__(self, x, y):
        # Image joueur
        self.image = pygame.image.load("Lior.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))

        # Hitbox
        self.rect = self.image.get_rect(topleft=(x, y))

        # Mouvement
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_force = -15
        self.gravity = 0.8
        self.on_ground = False

        # Stats
        self.lives = 3
        self.score = 0
        self.has_weapon = False

        # Invincibilité temporaire
        self.invincible = False
        self.invincible_timer = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_z]) and self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += self.gravity

    def move_and_collide(self, ground, platforms, obstacles):
        all_solids = [ground] + platforms + obstacles

        # Collision obstacles dangereux
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle) and not self.invincible:
                self.lives -= 1
                self.rect.topleft = (100, 470)  # respawn
                self.invincible = True
                self.invincible_timer = 60

        # Déplacement horizontal
        self.rect.x += self.vel_x
        for solid in all_solids:
            if self.rect.colliderect(solid):
                if self.vel_x > 0:
                    self.rect.right = solid.left
                elif self.vel_x < 0:
                    self.rect.left = solid.right

        # Déplacement vertical
        self.on_ground = False
        self.rect.y += self.vel_y
        for solid in all_solids:
            if self.rect.colliderect(solid):
                if self.vel_y > 0:
                    self.rect.bottom = solid.top
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = solid.bottom
                self.vel_y = 0

    def update(self, ground, platforms, obstacles):
        self.handle_input()
        self.apply_gravity()
        self.move_and_collide(ground, platforms, obstacles)

        # Timer invincibilité
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)