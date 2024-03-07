import pygame
import random
import sys
import os


def close_arkanoid(f):  # Выход из игры
    f.close()
    pygame.quit()
    sys.exit()


def get_mouse_x():  # Функция для нахождения абсциссы указателя в данный момент.
    return pygame.mouse.get_pos()[0]


def get_mouse_y():  # Функция для нахождения ординаты указателя в данный момент.
    return pygame.mouse.get_pos()[1]


def load_theme():  # Собственно Плеер.
    music_theme = random.randint(1, 5)
    music = {1: "ErrorRate", 2: "Humdrum", 3: "Ictus", 4: "Plunge", 5: "Zigzag"}
    music_to_load = os.path.join("audio", "themes", f"Viscid_{music[music_theme]}.mp3")
    pygame.mixer.music.load(music_to_load)
    return music_to_load
