import pygame
from levels import Level1


# Initialisation
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lior's Adventures")
clock = pygame.time.Clock()

# Couleurs de base
WHITE = (255, 255, 255)
BLACK = (20, 20, 30)

# Thèmes
themes = {
    "Bleu": {"bg": BLACK, "btn_base": (30,100,200), "btn_hover": (50,150,255), "title": (50,150,255)},
    "Rouge": {"bg": BLACK, "btn_base": (200,30,30), "btn_hover": (255,80,80), "title": (255,80,80)},
    "Vert": {"bg": BLACK, "btn_base": (30,200,30), "btn_hover": (80,255,80), "title": (80,255,80)}
}
current_theme = themes["Bleu"]

# Polices
title_font = pygame.font.SysFont("comicsansms", 80, bold=True)
button_font = pygame.font.SysFont("comicsansms", 40, bold=True)

# Boutons du menu
button_width, button_height = 300, 70
play_button = pygame.Rect((WIDTH - button_width)//2, 250, button_width, button_height)
settings_button = pygame.Rect((WIDTH - button_width)//2, 350, button_width, button_height)
quit_button = pygame.Rect((WIDTH - button_width)//2, 450, button_width, button_height)

# Boutons paramètres
theme_buttons = []
y = 200
for theme_name in themes:
    rect = pygame.Rect((WIDTH - button_width)//2, y, button_width, button_height)
    theme_buttons.append((rect, theme_name))
    y += 100
back_button = pygame.Rect((WIDTH - button_width)//2, 500, button_width, button_height)

# États du menu
running = True
menu = True
in_settings = False
level = None

def draw_button(rect, text, mouse_pos, base_color, hover_color):
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect, border_radius=12)
    else:
        pygame.draw.rect(screen, base_color, rect, border_radius=12)
    label = button_font.render(text, True, WHITE)
    screen.blit(label, (rect.x + (rect.width - label.get_width())//2,
                        rect.y + (rect.height - label.get_height())//2))

while running:
    mouse_pos = pygame.mouse.get_pos()
    screen.fill(current_theme["bg"])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if menu:
                if play_button.collidepoint(event.pos):
                    print("Jouer cliqué !")
                    menu = False
                if settings_button.collidepoint(event.pos):
                    in_settings = True
                    menu = False
                if quit_button.collidepoint(event.pos):
                    running = False
            elif in_settings:
                for rect, theme_name in theme_buttons:
                    if rect.collidepoint(event.pos):
                        current_theme = themes[theme_name]
                        print(f"Thème changé : {theme_name}")
                if back_button.collidepoint(event.pos):
                    menu = True
                    in_settings = False

    if menu:
        # Menu principal
        title_text = title_font.render("Lior's Adventures", True, current_theme["title"])
        screen.blit(title_text, ((WIDTH - title_text.get_width())//2, 100))

        draw_button(play_button, "Jouer", mouse_pos,
                    current_theme["btn_base"], current_theme["btn_hover"])
        draw_button(settings_button, "Paramètres", mouse_pos,
                    current_theme["btn_base"], current_theme["btn_hover"])
        draw_button(quit_button, "Quitter", mouse_pos,
                    current_theme["btn_base"], current_theme["btn_hover"])

    elif in_settings:
        # Écran Paramètres
        settings_text = title_font.render("Paramètres", True, current_theme["title"])
        screen.blit(settings_text, ((WIDTH - settings_text.get_width())//2, 50))

        # Boutons thèmes
        for rect, theme_name in theme_buttons:
            draw_button(rect, theme_name, mouse_pos,
                        current_theme["btn_base"], current_theme["btn_hover"])

        draw_button(back_button, "Retour", mouse_pos,
                    current_theme["btn_base"], current_theme["btn_hover"])
    else:
        # Écran jeu → Niveau 1
        if level is None:
            level = Level1(screen)

    level.update()
    level.draw()



    pygame.display.flip()
    clock.tick(60)

pygame.quit()