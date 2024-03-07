import pygame
import os
import math


pygame.init()


class Ball(pygame.sprite.Sprite):
    """На самом деле это квадрат"""

    speed = 0
    x = 0
    y = 0
    directions = [120, 140, 160, 180, 200, 220, 240]
    direction = 0
    width = 20
    height = 20
    bounce = pygame.mixer.Sound(os.path.join("audio", "sounds", "bounce.wav"))

    def __init__(self):  # Создание мячика
        super().__init__()
        self.image = pygame.image.load(os.path.join("images", "ball", "dark_theme",
                                                    "ballframe1.png"))
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

    def horizontal_bounce(self, bounce, d=0):  # Горизонтальный отскок мячика
        self.direction = (180 - self.direction) % 360
        self.direction -= d
        bounce.play()

    def vertical_bounce(self, bounce):  # Вертикальный отскок мячика
        self.direction = (360 - self.direction) % 360
        bounce.play()

    def update(self):  # Движение мячика
        if self.direction < 0:
            self.direction += 360
        if self.direction >= 360:
            self.direction -= 360
        direction_radians = math.radians(self.direction)
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)
        self.rect.x = self.x
        self.rect.y = self.y
        if self.y <= 0:
            self.horizontal_bounce(pygame.mixer.Sound(os.path.join("audio", "sounds", "bounce.wav")))
            self.y = 1
        if self.x <= 0:
            self.vertical_bounce(pygame.mixer.Sound(os.path.join("audio", "sounds", "bounce.wav")))
            self.x = 1
        if self.x > self.screenwidth - self.width:
            self.vertical_bounce(pygame.mixer.Sound(os.path.join("audio", "sounds", "bounce.wav")))
            self.x = self.screenwidth - self.width - 1
        if self.y > 600:
            return True
        else:
            return False
