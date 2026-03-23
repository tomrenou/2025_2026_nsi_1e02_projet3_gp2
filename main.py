import tkinter as tk
import pygame

# Taille de la fenêtre
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Créer la fenêtre
root = tk.Tk()
root.title("nom du jeu à trouver")

# Créer le canvas pour dessiner le jeu
canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
canvas.pack()

# Boucle principale
root.mainloop()