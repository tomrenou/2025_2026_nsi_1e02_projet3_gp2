import pygame

WHITE = (255, 255, 255)

class Player:
    def __init__(self, x, y):
        # Charge l'image
        self.image = pygame.image.load("Lior.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 80))

        # La hitbox
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.speed = 5
        self.jump_force = -15
        self.gravity = 0.8

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
        all_solids = [ground] + platforms

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

    def draw(self, screen):
        screen.blit(self.image, self.rect)
