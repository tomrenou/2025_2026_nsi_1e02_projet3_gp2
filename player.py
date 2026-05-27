import pygame

WHITE = (255, 255, 255)

class Player:
    def __init__(self, x, y, image_path="Liorbleu.png"):

        # Image joueur
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 60))

        # Hitbox
        self.rect = self.image.get_rect(topleft=(x, y))

        # Mouvement
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 2
        self.jump_force = -14
        self.gravity = 0.8
        self.on_ground = False

        # Stats
        self.lives = 3
        self.score = 0

        # Arme
        self.has_weapon = False
        self.bullets = []

        self.shoot_cooldown = 0
        self.ammo = 6
        self.max_ammo = 6

        self.reloading = False
        self.reload_timer = 0

        # Invincibilité temporaire
        self.invincible = False
        self.invincible_timer = 0

    def handle_input(self):

        keys = pygame.key.get_pressed()
        self.vel_x = 0

        # Déplacements
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.vel_x = -self.speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed

        # Saut
        if (
            keys[pygame.K_SPACE]
            or keys[pygame.K_UP]
            or keys[pygame.K_z]
        ) and self.on_ground:

            self.vel_y = self.jump_force
            self.on_ground = False

        # Tir
        if (
            keys[pygame.K_f]
            and self.has_weapon
            and self.shoot_cooldown == 0
            and self.ammo > 0
            and not self.reloading
        ):

            bullet = pygame.Rect(
                self.rect.centerx,
                self.rect.centery,
                15,
                5
            )

            self.bullets.append(bullet)

            self.shoot_cooldown = 20
            self.ammo -= 1

        # Rechargement
        if (
            keys[pygame.K_r]
            and self.ammo < self.max_ammo
            and not self.reloading
        ):

            self.reloading = True
            self.reload_timer = 120

    def apply_gravity(self):
        self.vel_y += self.gravity

    def move_and_collide(self, ground, platforms, obstacles):

        all_solids = [ground] + platforms + obstacles

        # Collision obstacles
        for obstacle in obstacles:

            if self.rect.colliderect(obstacle) and not self.invincible:

                self.lives -= 1

                self.rect.topleft = (180, 190)

                self.invincible = True
                self.invincible_timer = 60

        # Horizontal
        self.rect.x += self.vel_x

        for solid in all_solids:

            if self.rect.colliderect(solid):

                if self.vel_x > 0:
                    self.rect.right = solid.left

                elif self.vel_x < 0:
                    self.rect.left = solid.right

        # Vertical
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

        self.move_and_collide(
            ground,
            platforms,
            obstacles
        )

        # Bullets
        for bullet in self.bullets:
            bullet.x += 10

        self.bullets = [
            bullet for bullet in self.bullets
            if bullet.x < 800
        ]

        # Cooldown tir
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # Invincibilité
        if self.invincible:

            self.invincible_timer -= 1

            if self.invincible_timer <= 0:
                self.invincible = False

        # Reload
        if self.reloading:

            self.reload_timer -= 1

            if self.reload_timer <= 0:

                self.ammo = self.max_ammo
                self.reloading = False

    def draw(self, screen):

        screen.blit(self.image, self.rect)

        for bullet in self.bullets:
            pygame.draw.rect(screen, (255, 255, 0), bullet)

    def draw_hud(self, screen):

        font = pygame.font.SysFont(None, 30)

        # Vies
        lives_text = font.render(
            f"Vies : {self.lives}",
            True,
            WHITE
        )

        screen.blit(lives_text, (10, 10))

        # Score
        score_text = font.render(
            f"Score : {self.score}",
            True,
            WHITE
        )

        screen.blit(score_text, (10, 40))

        # Munitions
        if self.reloading:

            ammo_text = font.render(
                "Rechargement...",
                True,
                (255, 165, 0)
            )

        else:

            ammo_text = font.render(
                f"Munitions : {self.ammo}/{self.max_ammo}",
                True,
                WHITE
            )

        screen.blit(ammo_text, (10, 70))