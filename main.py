import pygame
from levels import Level1

# Initialisation
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lior's Adventures")
clock = pygame.time.Clock()
# Couleurs
WHITE = (255, 255, 255)
BLACK = (20, 20, 30)
# Thèmes
themes = {
    "Bleu": {
        "bg": BLACK,
        "btn_base": (30, 100, 200),
        "btn_hover": (50, 150, 255),
        "title": (50, 150, 255)
    },

    "Rouge": {
        "bg": BLACK,
        "btn_base": (200, 30, 30),
        "btn_hover": (255, 80, 80),
        "title": (255, 80, 80)
    },

    "Vert": {
        "bg": BLACK,
        "btn_base": (30, 200, 30),
        "btn_hover": (80, 255, 80),
        "title": (80, 255, 80)
    }
}
current_theme = themes["Bleu"]

# Polices
title_font = pygame.font.SysFont("comicsansms", 80, bold=True)
button_font = pygame.font.SysFont("comicsansms", 40, bold=True)
char_font = pygame.font.SysFont(
    "comicsansms",
    31,
    bold=True
)
small_back_font = pygame.font.SysFont(
    "comicsansms",
    28,
    bold=True
)

# Couleurs des persos
character_colors = {
    "Lior": (255, 255, 255),
    "Lior de glace": (100, 200, 255),
    "Lior ténébreux": (80, 0, 120),
    "Lior de feu": (255, 80, 0)
}

# Images des persos
character_images = {
    "Lior":
        pygame.transform.scale(
            pygame.image.load("Liorbleu.png").convert_alpha(),
            (200, 200)
        ),
    "Lior de glace":
        pygame.transform.scale(
            pygame.image.load("Lior_glace.png").convert_alpha(),
            (200, 200)
        ),
    "Lior ténébreux":
        pygame.transform.scale(
            pygame.image.load("Lior_tenebreux.png").convert_alpha(),
            (200, 200)
        ),
    "Lior de feu":
        pygame.transform.scale(
            pygame.image.load("Lior_feu.png").convert_alpha(),
            (200, 200)
        ),
}
# Chemins des images
character_paths = {
    "Lior": "Liorbleu.png",
    "Lior de glace": "Lior_glace.png",
    "Lior ténébreux": "Lior_tenebreux.png",
    "Lior de feu": "Lior_feu.png",
}

# Boutons menu principal
button_width = 300
button_height = 70

play_button = pygame.Rect(
    (WIDTH - button_width) // 2,
    250,
    button_width,
    button_height
)
settings_button = pygame.Rect(
    (WIDTH - button_width) // 2,
    350,
    button_width,
    button_height
)
quit_button = pygame.Rect(
    (WIDTH - button_width) // 2,
    450,
    button_width,
    button_height
)
# Boutons paramètres
colors_button = pygame.Rect(
    (WIDTH - button_width) // 2,
    200,
    button_width,
    button_height
)
character_button = pygame.Rect(
    (WIDTH - button_width) // 2,
    300,
    button_width,
    button_height
)
fullscreen_button = pygame.Rect(
    (WIDTH - button_width) // 2,
    400,
    button_width,
    button_height
)
back_button = pygame.Rect(
    (WIDTH - button_width) // 2,
    500,
    button_width,
    button_height
)
# Retour perso
back_button_char = pygame.Rect(
    (WIDTH - 200) // 2,
    520,
    200,
    50
)
# Sous menu couleurs
theme_buttons = []
y = 200
for theme_name in themes:
    rect = pygame.Rect(
        (WIDTH - button_width) // 2,
        y,
        button_width,
        button_height
    )
    theme_buttons.append((rect, theme_name))
    y += 100
# Choix personnages
character_choices = [
    ("Lior",
     pygame.Rect(50, 200, 250, 60)),

    ("Lior de glace",
     pygame.Rect(50, 280, 250, 60)),

    ("Lior ténébreux",
     pygame.Rect(50, 360, 250, 60)),

    ("Lior de feu",
     pygame.Rect(50, 440, 250, 60)),
]
# Aperçu personnage
preview_rect = pygame.Rect(
    370,
    170,
    390,
    340
)
# États
running = True

menu = True
in_settings = False
in_color_menu = False
in_character_menu = False

# Variables
fullscreen = False
selected_character = "Lior"
level = None
def draw_button(
    rect,
    text,
    mouse_pos,
    base_color,
    hover_color,
    font=None
):
    if font is None:
        font = button_font
    if rect.collidepoint(mouse_pos):

        pygame.draw.rect(
            screen,
            hover_color,
            rect,
            border_radius=12
        )
    else:

        pygame.draw.rect(
            screen,
            base_color,
            rect,
            border_radius=12
        )
    label = font.render(text, True, WHITE)
    screen.blit(
        label,
        (
            rect.x + (rect.width - label.get_width()) // 2,
            rect.y + (rect.height - label.get_height()) // 2
        )
    )
def draw_rounded_rect_outline(
    surface,
    color,
    rect,
    radius,
    width=3
):
    pygame.draw.rect(
        surface,
        color,
        rect,
        width=width,
        border_radius=radius
    )

while running:
    mouse_pos = pygame.mouse.get_pos()
    screen.fill(current_theme["bg"])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # MENU PRINCIPAL
            if menu:
                if play_button.collidepoint(event.pos):
                    menu = False
                    level = Level1(
                        screen,
                        character_paths[selected_character]
                    )
                if settings_button.collidepoint(event.pos):
                    in_settings = True
                    menu = False
                if quit_button.collidepoint(event.pos):

                    running = False
            # PARAMÈTRES
            elif in_settings:
                if colors_button.collidepoint(event.pos):

                    in_settings = False
                    in_color_menu = True
                if character_button.collidepoint(event.pos):
                    in_settings = False
                    in_character_menu = True
                if fullscreen_button.collidepoint(event.pos):
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode(
                            (WIDTH, HEIGHT),
                            pygame.FULLSCREEN
                        )
                    else:
                        screen = pygame.display.set_mode(
                            (WIDTH, HEIGHT)
                        )
                if back_button.collidepoint(event.pos):
                    menu = True
                    in_settings = False
            # MENU COULEURS
            elif in_color_menu:
                for rect, theme_name in theme_buttons:
                    if rect.collidepoint(event.pos):
                        current_theme = themes[theme_name]
                if back_button.collidepoint(event.pos):
                    in_color_menu = False
                    in_settings = True
            # MENU PERSONNAGES
            elif in_character_menu:

                for name, rect in character_choices:

                    if rect.collidepoint(event.pos):

                        selected_character = name

                if back_button_char.collidepoint(event.pos):

                    in_character_menu = False
                    in_settings = True

    # MENU PRINCIPAL
    if menu:

        title_text = title_font.render(
            "Lior's Adventures",
            True,
            current_theme["title"]
        )

        screen.blit(
            title_text,
            (
                (WIDTH - title_text.get_width()) // 2,
                100
            )
        )

        draw_button(
            play_button,
            "Jouer",
            mouse_pos,
            current_theme["btn_base"],
            current_theme["btn_hover"]
        )

        draw_button(
            settings_button,
            "Paramètres",
            mouse_pos,
            current_theme["btn_base"],
            current_theme["btn_hover"]
        )

        draw_button(
            quit_button,
            "Quitter",
            mouse_pos,
            current_theme["btn_base"],
            current_theme["btn_hover"]
        )

    # PARAMÈTRES
    elif in_settings:

        settings_text = title_font.render(
            "Paramètres",
            True,
            current_theme["title"]
        )

        screen.blit(
            settings_text,
            (
                (WIDTH - settings_text.get_width()) // 2,
                50
            )
        )

        draw_button(
            colors_button,
            "Couleurs",
            mouse_pos,
            current_theme["btn_base"],
            current_theme["btn_hover"]
        )

        draw_button(
            character_button,
            "Personnage",
            mouse_pos,
            current_theme["btn_base"],
            current_theme["btn_hover"]
        )

        draw_button(
            fullscreen_button,
            "Plein écran" if not fullscreen else "Fenêtré",
            mouse_pos,
            current_theme["btn_base"],
            current_theme["btn_hover"]
        )

        draw_button(
            back_button,
            "Retour",
            mouse_pos,
            current_theme["btn_base"],
            current_theme["btn_hover"]
        )

    # MENU COULEURS
    elif in_color_menu:
        settings_text = title_font.render(
            "Couleurs",
            True,
            current_theme["title"]
        )
        screen.blit(
            settings_text,
            (
                (WIDTH - settings_text.get_width()) // 2,
                50
            )
        )
        for rect, theme_name in theme_buttons:
            draw_button(
                rect,
                theme_name,
                mouse_pos,
                current_theme["btn_base"],
                current_theme["btn_hover"]
            )
        draw_button(
            back_button,
            "Retour",
            mouse_pos,
            current_theme["btn_base"],
            current_theme["btn_hover"]
        )

    # MENU PERSONNAGES
    elif in_character_menu:
        settings_text = title_font.render(
            "Personnages",
            True,
            current_theme["title"]
        )
        screen.blit(
            settings_text,
            (
                (WIDTH - settings_text.get_width()) // 2,
                50
            )
        )
        # Boutons
        for name, rect in character_choices:
            draw_button(
                rect,
                name,
                mouse_pos,
                current_theme["btn_base"],
                current_theme["btn_hover"],
                font=char_font
            )
        # Cadre
        draw_rounded_rect_outline(
            screen,
            character_colors[selected_character],
            preview_rect,
            radius=18
        )
        # Image perso
        img = character_images[selected_character]
        img_x = (
            preview_rect.x
            + (preview_rect.width - img.get_width()) // 2
        )
        img_y = (
            preview_rect.y
            + (preview_rect.height - img.get_height()) // 2
        )
        screen.blit(img, (img_x, img_y))
        draw_button(
            back_button_char,
            "Retour",
            mouse_pos,
            current_theme["btn_base"],
            current_theme["btn_hover"],
            font=small_back_font
        )
    # JEU
    else:
        level.update()
        level.draw()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()