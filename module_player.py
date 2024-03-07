import pygame
import os
import random
from pygame.locals import *


movemode = False


class Player(pygame.sprite.Sprite):
    """Плеер - дальше. Это Ракетка."""

    def __init__(self):  # Создание ракетки
        super().__init__()
        self.width = 100
        self.height = 15
        self.image = pygame.image.load(os.path.join("images", "player", "dark_theme",
                                                    "playerframe1.png"))
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        self.rect.x = random.randint(0, 700)
        self.rect.y = self.screenheight - self.height - 5
        self.movemode = 0

    def update(self):  # Движение ракетки
        if pygame.key.get_pressed()[K_UP] or pygame.key.get_pressed()[K_w]:
            if self.rect.y > 450:
                self.rect.y -= 2
        if pygame.key.get_pressed()[K_DOWN] or pygame.key.get_pressed()[K_s]:
            if self.rect.y < 580:
                self.rect.y += 2
        if movemode:  # Движение ракетки с помощью кнопок. Это неудобно.
            if pygame.key.get_pressed()[K_LEFT] or pygame.key.get_pressed()[K_a]:
                if self.rect.x >= 5:
                    self.rect.x -= 5
            if pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed()[K_d]:
                if self.rect.x <= 695:
                    self.rect.x += 5
        else:  # По умолчанию игрок управляет ракеткой мышью
            self.rect.x = pygame.mouse.get_pos()[0]
            if self.rect.x > self.screenwidth - self.width:
                self.rect.x = self.screenwidth - self.width
