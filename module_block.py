import pygame
import os


pygame.init()


class Block(pygame.sprite.Sprite):
    """Класс для всех этих радужных блоков, которые нужно сбивать"""

    def __init__(self, color, x, y):  # Создание блока
        super().__init__()
        self.image = pygame.image.load(os.path.join("images", "blocks",
                                                    f"{color}block.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
