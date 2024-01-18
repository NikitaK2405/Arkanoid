import math
import os
import random
import sys
import pygame
from pygame.locals import *

theme = "DARK"
# Цвета
black = (0, 0, 0)
green = (0, 255, 0)
lightgrey = (145, 145, 145)
darkgrey = (110, 110, 110)
red = (225, 0, 0)
white = (255, 255, 255)
colors = ["red", "orange", "yellow", "green", "lightblue", "blue", "purple"]  # Цвета блоков

# Размеры блоков
block_width = 23
block_height = 15

# Размеры решётки блоков
ncolumn = 32
nrow = 4

pygame.init()  # Инициализация Pygame

# Параметры экрана
screen = pygame.display.set_mode([800, 600])
background = pygame.Surface(screen.get_size())
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.set_caption("Arkanoid")
icon = pygame.Surface((10, 10))
pygame.display.set_icon(icon)
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
clock = pygame.time.Clock()
fps = 90

# Шрифты
font = pygame.font.SysFont('Courier', 45, bold=True)
mediumfont = pygame.font.SysFont('Courier', 36, bold=True)
smallfont = pygame.font.SysFont('Courier', 35, bold=True)

# Звуки
whoosh = pygame.mixer.Sound(os.path.join("audio", "sounds", "introwhoosh.wav"))
bounce = pygame.mixer.Sound(os.path.join("audio", "sounds", "bounce.wav"))
music_themes = [1, 2, 3, 4, 5]

start = False
paused = False

if theme == "DARK":
    xtext = smallfont.render("X", True, white)
else:
    xtext = smallfont.render("X", True, black)
xpos = xtext.get_rect(centerx=775)
xpos.top = 5


class Block(pygame.sprite.Sprite):
    """Класс для всех этих радужных блоков, которые нужно сбивать"""

    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join("images",
                                                    "blocks",
                                                    f"{color}block.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ball(pygame.sprite.Sprite):
    """На самом деле это квадрат"""

    speed = 0
    x = 0
    y = 0
    directions = [60, 120, 240, 300]
    direction = 0
    width = 20
    height = 20

    def __init__(self):
        super().__init__()
        if theme == "DARK":
            self.image = pygame.image.load(os.path.join("images",
                                                        "ball",
                                                        "dark_theme",
                                                        "ballframe1.png"))
        else:
            self.image = pygame.image.load(os.path.join("images",
                                                        "ball",
                                                        "light_theme",
                                                        "ballframe1.png"))
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

    def bounce(self, d):  # Горизонтальный отскок мячика
        self.direction = (180 - self.direction) % 360
        self.direction -= d
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
            self.bounce(0)
            self.y = 1
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            bounce.play()
            self.x = 1
        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            bounce.play()
            self.x = self.screenwidth - self.width - 1
        if self.y > 600:
            return True
        else:
            return False


class Player(pygame.sprite.Sprite):
    """Плеер - дальше. Это Ракетка."""

    def __init__(self):
        super().__init__()
        self.width = 100
        self.height = 15
        if theme == "DARK":
            self.image = pygame.image.load(os.path.join("images",
                                                        "player",
                                                        "dark_theme",
                                                        "playerframe1.png"))
        else:
            self.image = pygame.image.load(os.path.join("images",
                                                        "player",
                                                        "light_theme",
                                                        "playerframe1.png"))
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        self.rect.x = random.randint(0, 725)
        self.rect.y = self.screenheight - self.height - 2
        self.movemode = 0

    def update(self):  # Движение ракетки
        if pygame.key.get_pressed()[K_UP]:
            if self.rect.y > 450:
                self.rect.y -= 2
        if pygame.key.get_pressed()[K_DOWN]:
            if self.rect.y < 580:
                self.rect.y += 2
        if movemode:
            if pygame.key.get_pressed()[K_LEFT]:
                if self.rect.x >= 5:
                    self.rect.x -= 5
            if pygame.key.get_pressed()[K_RIGHT]:
                if self.rect.x <= 695:
                    self.rect.x += 5
        else:
            self.rect.x = get_mouse_x()
            if self.rect.x > self.screenwidth - self.width:
                self.rect.x = self.screenwidth - self.width


player = Player()  # Создание ракетки
ball = Ball()  # Создание мячика
startballpos = 180

# Добавление спрайтов в группы
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
balls.add(ball)
allsprites = pygame.sprite.Group()
allsprites.add(player)
allsprites.add(ball)


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


def pausecheck():  # Огромная функция, отвечающая за паузу
    global event,       \
        paused,         \
        game_over,      \
        result,         \
        nextlevel,      \
        score,          \
        allsprites,     \
        blocks,         \
        nrow,           \
        level,          \
        ballframe,      \
        playerframe,    \
        framecount,     \
        theme,          \
        xtext
    while paused:
        pauseclose = False
        fog = pygame.Surface((800, 600))  # Затемняющая поверхность
        if theme == "DARK":
            xtext = smallfont.render("X", True, white)
            pausetext = smallfont.render("||", True, white)
            item1 = smallfont.render("resume (Esc)", True, white)
            item2 = smallfont.render("new game (N)", True, white)
            item3 = smallfont.render("exit (AltF4)", True, white)
        else:
            xtext = smallfont.render("X", True, black)
            pausetext = smallfont.render("||", True, black)
            item1 = smallfont.render("resume (Esc)", True, black)
            item2 = smallfont.render("new game (N)", True, black)
            item3 = smallfont.render("exit (AltF4)", True, black)
        pausepos = pausetext.get_rect(centerx=25)
        pausepos.top = 5
        item1pos = item1.get_rect(centerx=background.get_width() / 2)
        item1pos.top = 300
        item2pos = item2.get_rect(centerx=background.get_width() / 2)
        item2pos.top = 350
        item3pos = item3.get_rect(centerx=background.get_width() / 2)
        item3pos.top = 400

        selected = 0
        while not pauseclose:
            if theme == "DARK":
                xtext = smallfont.render("X", True, white)
                pausetext = smallfont.render("||", True, white)
                if selected != 1:
                    item1 = smallfont.render("resume (Esc)", True, white)
                if selected != 2:
                    item2 = smallfont.render("new game (N)", True, white)
                if selected != 3:
                    item3 = smallfont.render("exit (AltF4)", True, white)
            else:
                xtext = smallfont.render("X", True, black)
                pausetext = smallfont.render("||", True, black)
                if selected != 1:
                    item1 = smallfont.render("resume (Esc)", True, black)
                if selected != 2:
                    item2 = smallfont.render("new game (N)", True, black)
                if selected != 3:
                    item3 = smallfont.render("exit (AltF4)", True, black)
            if speedup:
                screen.blit(xtext, xpos)
            fog.set_alpha(200)
            if theme == "DARK":
                fog.fill(black)
            else:
                fog.fill(white)
            allsprites.draw(screen)
            screen.blit(fog, (0, 0))
            screen.blit(pausetext, pausepos)
            screen.blit(item1, item1pos)
            screen.blit(item2, item2pos)
            screen.blit(item3, item3pos)

            for event in pygame.event.get():  # Проверка событий
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_LALT or event.key == K_RALT:
                        if event.mod == KMOD_ALT:
                            if event.key == K_F4:
                                pygame.quit()
                                sys.exit()
                    if event.key == K_t:
                        if theme == "LIGHT":
                            theme = "DARK"
                        else:
                            theme = "LIGHT"
                    if event.key == K_ESCAPE:
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)
                        pygame.mixer.music.set_volume(volume)
                        if pygame.mixer.music.get_endevent():
                            pygame.mixer.music.queue(load_theme())
                        paused = False
                        pauseclose = True
                    if event.key == K_n:
                        if theme == "DARK":
                            screen.fill(black)
                        else:
                            screen.fill(white)
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)
                        pygame.mixer.music.set_volume(volume)
                        pygame.mixer.music.stop()
                        pygame.mixer.music.queue(load_theme())
                        paused = False
                        pauseclose = True
                        result = None
                        game_over = True
                        nextlevel = False
                        nrow = 4
                        score = 0
                        level = 1
                        deadblocks.clear()
                        allsprites = pygame.sprite.Group()
                        allsprites.add(ball)
                        allsprites.add(player)
                        blocks = pygame.sprite.Group()
                if event.type == pygame.MOUSEMOTION:
                    if item1pos.left <= get_mouse_x() <= item1pos.right and \
                            item1pos.top <= get_mouse_y() <= item1pos.bottom:
                        if theme == "DARK":
                            item1 = mediumfont.render("resume (Esc)", True, lightgrey)
                            item2 = smallfont.render("new game (N)", True, white)
                            item3 = smallfont.render("exit (AltF4)", True, white)
                        else:
                            item1 = mediumfont.render("resume (Esc)", True, darkgrey)
                            item2 = smallfont.render("new game (N)", True, black)
                            item3 = smallfont.render("exit (AltF4)", True, black)
                        item1pos = item1.get_rect(centerx=background.get_width() / 2)
                        item1pos.top = 300
                        item2pos = item2.get_rect(centerx=background.get_width() / 2)
                        item2pos.top = 350
                        item3pos = item3.get_rect(centerx=background.get_width() / 2)
                        item3pos.top = 400
                        selected = 1

                    elif item2pos.left <= get_mouse_x() <= item2pos.right and \
                            item2pos.top <= get_mouse_y() <= item2pos.bottom:
                        if theme == "DARK":
                            item1 = smallfont.render("resume (Esc)", True, white)
                            item2 = mediumfont.render("new game (N)", True, lightgrey)
                            item3 = smallfont.render("exit (AltF4)", True, white)
                        else:
                            item1 = smallfont.render("resume (Esc)", True, black)
                            item2 = mediumfont.render("new game (N)", True, darkgrey)
                            item3 = smallfont.render("exit (AltF4)", True, black)
                        item1pos = item1.get_rect(centerx=background.get_width() / 2)
                        item1pos.top = 300
                        item2pos = item2.get_rect(centerx=background.get_width() / 2)
                        item2pos.top = 350
                        item3pos = item3.get_rect(centerx=background.get_width() / 2)
                        item3pos.top = 400
                        selected = 2

                    elif item3pos.left <= get_mouse_x() <= item3pos.right and \
                            item3pos.top <= get_mouse_y() <= item3pos.bottom:
                        if theme == "DARK":
                            item1 = smallfont.render("resume (Esc)", True, white)
                            item2 = smallfont.render("new game (N)", True, white)
                            item3 = mediumfont.render("exit (AltF4)", True, lightgrey)
                        else:
                            item1 = smallfont.render("resume (Esc)", True, black)
                            item2 = smallfont.render("new game (N)", True, black)
                            item3 = mediumfont.render("exit (AltF4)", True, darkgrey)
                        item1pos = item1.get_rect(centerx=background.get_width() / 2)
                        item1pos.top = 300
                        item2pos = item2.get_rect(centerx=background.get_width() / 2)
                        item2pos.top = 350
                        item3pos = item3.get_rect(centerx=background.get_width() / 2)
                        item3pos.top = 400
                        selected = 3

                    else:
                        if theme == "DARK":
                            item1 = smallfont.render("resume (Esc)", True, white)
                            item2 = smallfont.render("new game (N)", True, white)
                            item3 = smallfont.render("exit (AltF4)", True, white)
                        else:
                            item1 = smallfont.render("resume (Esc)", True, black)
                            item2 = smallfont.render("new game (N)", True, black)
                            item3 = smallfont.render("exit (AltF4)", True, black)
                        item1pos = item1.get_rect(centerx=background.get_width() / 2)
                        item1pos.top = 300
                        item2pos = item2.get_rect(centerx=background.get_width() / 2)
                        item2pos.top = 350
                        item3pos = item3.get_rect(centerx=background.get_width() / 2)
                        item3pos.top = 400
                        selected = 0

                if selected == 1:  # Продолжение игры
                    if event.type == MOUSEBUTTONUP:
                        if item1pos.left <= get_mouse_x() <= item1pos.right and \
                                item1pos.top <= get_mouse_y() <= item1pos.bottom:
                            pygame.mouse.set_visible(False)
                            pygame.event.set_grab(True)
                            pygame.mixer.music.set_volume(volume)
                            if pygame.mixer.music.get_endevent():
                                pygame.mixer.music.queue(load_theme())
                            paused = False
                            pauseclose = True

                elif selected == 2:  # Новая игра
                    if event.type == MOUSEBUTTONUP:
                        if item2pos.left <= get_mouse_x() <= item2pos.right and \
                                item2pos.top <= get_mouse_y() <= item2pos.bottom:
                            if theme == "DARK":
                                screen.fill(black)
                            else:
                                screen.fill(white)
                            pygame.mouse.set_visible(False)
                            pygame.event.set_grab(True)
                            pygame.mixer.music.set_volume(volume)
                            pygame.mixer.music.stop()
                            pygame.mixer.music.queue(load_theme())
                            paused = False
                            pauseclose = True
                            result = None
                            game_over = True
                            nextlevel = False
                            nrow = 4
                            score = 0
                            level = 1
                            deadblocks.clear()
                            allsprites = pygame.sprite.Group()
                            allsprites.add(ball)
                            allsprites.add(player)
                            blocks = pygame.sprite.Group()

                elif selected == 3:  # Выход из игры
                    if event.type == MOUSEBUTTONUP:
                        if item3pos.left <= get_mouse_x() <= item3pos.right and \
                                item3pos.top <= get_mouse_y() <= item3pos.bottom:
                            pygame.quit()
                            sys.exit()

            pygame.display.flip()
            clock.tick(fps)


def intro():  # Приветственный экран в начале игры
    global start, i, event, theme
    whoosh.play()

    while not start:
        for i in range(0, 255, 2):
            text = smallfont.render("Press any key to start the game", True, (i, i, i))
            textpos = text.get_rect(centerx=background.get_width() / 2)
            textpos.top = 450

            for event in pygame.event.get():  # Проверка событий
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    start = True
                    break
                if event.type == KEYDOWN:
                    if event.key == K_LALT or event.key == K_RALT:
                        if event.mod == KMOD_ALT:
                            if event.key == K_F4:
                                pygame.quit()
                                sys.exit()
                    if event.key == K_t:
                        if theme == "LIGHT":
                            theme = "DARK"
                        else:
                            theme = "LIGHT"
                    elif event.key != K_LALT and event.key != K_RALT:
                        start = True
                        break
            if start:
                load_theme()
                pygame.mixer.music.queue(load_theme())
                pygame.mixer.music.play()
                break

            clock.tick(fps)
            if theme == "DARK":
                screen.fill(black)
            else:
                screen.fill(white)
            screen.blit(text, textpos)
            pygame.display.flip()

        for i in range(255, 0, -2):
            text = smallfont.render("Press any key to start the game", True, (i, i, i))
            textpos = text.get_rect(centerx=background.get_width() / 2)
            textpos.top = 450

            for event in pygame.event.get():  # Проверка событий
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    start = True
                    break
                if event.type == KEYDOWN:
                    if event.key == K_LALT or event.key == K_RALT:
                        if event.mod == KMOD_ALT:
                            if event.key == K_F4:
                                pygame.quit()
                                sys.exit()
                    if event.key == K_t:
                        if theme == "LIGHT":
                            theme = "DARK"
                        else:
                            theme = "LIGHT"
                    elif event.key != K_LALT and event.key != K_RALT:
                        start = True
                        break
            if start:
                load_theme()
                pygame.mixer.music.queue(load_theme())
                pygame.mixer.music.play()
                break

            clock.tick(fps)
            if theme == "DARK":
                screen.fill(black)
            else:
                screen.fill(white)
            screen.blit(text, textpos)
            pygame.display.flip()


intro()  # Отображение начального экрана

deadblocks = []
score = 0
level = 1
ballframe = 1
playerframe = 1
framecount = 1

result = None
shift = False

currentspeed = ball.speed
volume = pygame.mixer.music.get_volume()

while True:
    game_over = False
    nextlevel = False
    speedup = False
    movemode = 0

    while not start:
        for i in range(0, 255, 2):
            text1 = smallfont.render("Press any key to start new game", True, (i, i, i))
            text1pos = text1.get_rect(centerx=background.get_width() / 2)
            text1pos.top = 450

            text2 = font.render("You win!", True, green)
            text2pos = text2.get_rect(centerx=background.get_width() / 2)
            text2pos.top = 300

            text3 = font.render("Game over", True, red)
            text3pos = text3.get_rect(centerx=background.get_width() / 2)
            text3pos.top = 300

            if theme == "DARK":
                text4 = smallfont.render(f"Your score is {score}", True, white)
            else:
                text4 = smallfont.render(f"Your score is {score}", True, black)
            text4pos = text4.get_rect(centerx=background.get_width() / 2)
            text4pos.top = 350

            for event in pygame.event.get():  # Проверка событий
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    start = True
                    deadblocks.clear()
                    allsprites = pygame.sprite.Group()
                    allsprites.add(ball)
                    allsprites.add(player)
                    blocks = pygame.sprite.Group()
                    break
                if event.type == KEYDOWN:
                    if event.key == K_LALT or event.key == K_RALT:
                        if event.mod == KMOD_ALT:
                            if event.key == K_F4:
                                pygame.quit()
                                sys.exit()
                    if event.key == K_t:
                        if theme == "LIGHT":
                            theme = "DARK"
                        else:
                            theme = "LIGHT"
                    elif event.key != K_LALT and event.key != K_RALT:
                        start = True
                        deadblocks.clear()
                        allsprites = pygame.sprite.Group()
                        allsprites.add(ball)
                        allsprites.add(player)
                        blocks = pygame.sprite.Group()
                        break
            if start:
                load_theme()
                pygame.mixer.music.queue(load_theme())
                pygame.mixer.music.play()
                break

            # Анимации конца игры
            if player.rect.y < 580:
                player.rect.y += 1
            for b in blocks:
                b.rect.y += random.randint(2, 4)

            clock.tick(fps)
            if theme == "DARK":
                screen.fill(black)
                player.image = pygame.image.load(os.path.join("images",
                                                              "player",
                                                              "dark_theme",
                                                              f"playerframe{playerframe}.png"))
            else:
                screen.fill(white)
                player.image = pygame.image.load(os.path.join("images",
                                                              "player",
                                                              "light_theme",
                                                              f"playerframe{playerframe}.png"))
            allsprites.remove(ball)
            allsprites.draw(screen)
            allsprites.add(ball)

            if not nextlevel:
                text1 = smallfont.render("Press any key to start new game", True, (i, i, i))
            else:
                text1 = smallfont.render("Press any key to start next level", True, (i, i, i))
            text1pos = text1.get_rect(centerx=background.get_width() / 2)
            text1pos.top = 450
            screen.blit(text1, text1pos)

            if result == "Victory":
                screen.blit(text2, text2pos)
                nextlevel = True

            elif result == "Defeat":
                if level == 1:
                    if theme == "DARK":
                        text4 = smallfont.render(f"Your score is {score}", True, white)
                    else:
                        text4 = smallfont.render(f"Your score is {score}", True, black)
                else:
                    if theme == "DARK":
                        text4 = smallfont.render(f"You reached level {level}", True, white)
                        text5 = smallfont.render(f"and your score is {score}", True, white)
                    else:
                        text4 = smallfont.render(f"You reached level {level}", True, black)
                        text5 = smallfont.render(f"and your score is {score}", True, black)
                    text5pos = text5.get_rect(centerx=background.get_width() / 2)
                    text5pos.top = 400
                    screen.blit(text5, text5pos)

                text4pos = text4.get_rect(centerx=background.get_width() / 2)
                text4pos.top = 350
                screen.blit(text3, text3pos)
                screen.blit(text4, text4pos)

            pygame.display.flip()

        for i in range(255, 0, -2):
            text1 = smallfont.render("Press any key to start new game", True, (i, i, i))
            text1pos = text1.get_rect(centerx=background.get_width() / 2)
            text1pos.top = 450

            text2 = font.render("You win!", True, green)
            text2pos = text2.get_rect(centerx=background.get_width() / 2)
            text2pos.top = 300

            text3 = font.render("Game over", True, red)
            text3pos = text3.get_rect(centerx=background.get_width() / 2)
            text3pos.top = 300

            if theme == "DARK":
                text4 = smallfont.render(f"Yor score is {score}", True, white)
            else:
                text4 = smallfont.render(f"Yor score is {score}", True, black)
            text4pos = text4.get_rect(centerx=background.get_width() / 2)
            text4pos.top = 350

            for event in pygame.event.get():  # Проверка событий
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    start = True
                    deadblocks.clear()
                    allsprites = pygame.sprite.Group()
                    allsprites.add(ball)
                    allsprites.add(player)
                    blocks = pygame.sprite.Group()
                    break
                if event.type == KEYDOWN:
                    if event.key == K_LALT or event.key == K_RALT:
                        if event.mod == KMOD_ALT:
                            if event.key == K_F4:
                                pygame.quit()
                                sys.exit()
                    if event.key == K_t:
                        if theme == "LIGHT":
                            theme = "DARK"
                        else:
                            theme = "LIGHT"
                    elif event.key != K_LALT and event.key != K_RALT:
                        start = True
                        deadblocks.clear()
                        allsprites = pygame.sprite.Group()
                        allsprites.add(ball)
                        allsprites.add(player)
                        blocks = pygame.sprite.Group()
                        break
            if start:
                load_theme()
                pygame.mixer.music.queue(load_theme())
                pygame.mixer.music.play()
                break

            # Анимации конца игры
            if player.rect.y < 580:
                player.rect.y += 1
            for b in blocks:
                if b.rect.y <= screen.get_height():
                    b.rect.y += random.randint(2, 4)

            clock.tick(fps)
            if theme == "DARK":
                screen.fill(black)
                player.image = pygame.image.load(os.path.join("images",
                                                              "player",
                                                              "dark_theme",
                                                              f"playerframe{playerframe}.png"))
            else:
                screen.fill(white)
                player.image = pygame.image.load(os.path.join("images",
                                                              "player",
                                                              "light_theme",
                                                              f"playerframe{playerframe}.png"))
            allsprites.remove(ball)
            allsprites.draw(screen)
            allsprites.add(ball)

            if not nextlevel:
                text1 = smallfont.render("Press any key to start new game", True, (i, i, i))
            else:
                text1 = smallfont.render("Press any key to start next level", True, (i, i, i))
            text1pos = text1.get_rect(centerx=background.get_width() / 2)
            text1pos.top = 450
            screen.blit(text1, text1pos)

            if result == "Victory":
                screen.blit(text2, text2pos)
                nextlevel = True

            elif result == "Defeat":
                if level == 1:
                    if theme == "DARK":
                        text4 = smallfont.render(f"Your score is {score}", True, white)
                    else:
                        text4 = smallfont.render(f"Your score is {score}", True, black)
                else:
                    if theme == "DARK":
                        text4 = smallfont.render(f"You reached level {level}", True, white)
                        text5 = smallfont.render(f"and your score is {score}", True, white)
                    else:
                        text4 = smallfont.render(f"You reached level {level}", True, black)
                        text5 = smallfont.render(f"and your score is {score}", True, black)
                    text5pos = text5.get_rect(centerx=background.get_width() / 2)
                    text5pos.top = 400
                    screen.blit(text5, text5pos)

                text4pos = text4.get_rect(centerx=background.get_width() / 2)
                text4pos.top = 350
                screen.blit(text3, text3pos)
                screen.blit(text4, text4pos)

            pygame.display.flip()

    if result == "Defeat":
        nrow = 4
        score = 0
        level = 1
    elif result == "Victory":
        level += 1

    top = 50
    ballframe = 1
    playerframe = 1
    framecount = 1
    player.rect.y = 580

    for row in range(nrow):  # Отрисовка блоков
        for column in range(ncolumn):
            block = Block(random.choice(colors), column * (block_width + 2) + 1, top)
            blocks.add(block)
            allsprites.add(block)
        top += block_height + 2

    ball.x = random.randint(20, 740)
    ball.y = startballpos
    ball.direction = random.choice(ball.directions)
    ball.speed = 1.2 + level / 10

    while not game_over:  # Главный игровой цикл
        clock.tick(fps)
        if theme == "DARK":
            screen.fill(black)
            xtext = smallfont.render("X", True, white)
        else:
            screen.fill(white)
            xtext = smallfont.render("X", True, black)

        if pygame.mixer.music.get_endevent():
            pygame.mixer.music.queue(load_theme())

        for event in pygame.event.get():  # Проверка событий
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LALT or event.key == K_RALT:
                    if event.mod == KMOD_ALT:
                        if event.key == K_F4:
                            pygame.quit()
                            sys.exit()
                if event.key == K_t:
                    if theme == "LIGHT":
                        theme = "DARK"
                    else:
                        theme = "LIGHT"
                if event.key == K_ESCAPE:
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)
                    pygame.mixer.music.set_volume(0)
                    paused = True
                if event.key == K_x:
                    speedup = not speedup
                    if speedup:
                        currentspeed = ball.speed
                        ball.speed *= 2
                    else:
                        ball.speed = currentspeed
                if event.key == K_LEFT or event.key == K_RIGHT:
                    movemode = 1
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    if player.rect.y > 450:
                        player.rect.y -= 5
                elif event.button == 5:
                    if player.rect.y < 580:
                        player.rect.y += 5
            if event.type == MOUSEMOTION:
                if movemode:
                    pygame.mouse.set_pos(player.rect.x, player.rect.y)
                movemode = 0

        pausecheck()

        if not ball.update():
            player.update()

        if ball.update() and len(blocks) > 0:  # Игрок не поймал мячик
            result = "Defeat"
            whoosh.play()
            pygame.mixer.music.stop()
            game_over = True

        if pygame.sprite.spritecollide(player, balls, False):  # Отскок мячика от ракетки
            x1, y1 = ball.rect.bottomleft
            x2, y2 = ball.rect.topright
            x3, y3 = player.rect.bottomleft
            x4, y4 = player.rect.topright

            width = min(x2, x4) - max(x1, x3)  # ширина пересечения
            height = min(y1, y3) - max(y2, y4)  # высота пересечения
            if width < height or ball.rect.top > player.rect.top:
                ball.direction = (360 - ball.direction) % 360
                bounce.play()
            else:
                ball.y -= 5
                difference = player.rect.centerx - ball.rect.centerx
                if difference > 30:
                    difference = 30
                ball.bounce(difference)
                ball.speed += 0.03

        deadblocks = pygame.sprite.spritecollide(ball, blocks, True)  # Список только что сбитых блоков

        if len(deadblocks) > 0:
            if len(deadblocks) == 1:
                hitted = deadblocks[0]
                x1, y1 = ball.rect.bottomleft
                x2, y2 = ball.rect.topright
                x3, y3 = hitted.rect.bottomleft
                x4, y4 = hitted.rect.topright
                width = min(x2, x4) - max(x1, x3)  # ширина пересечения
                height = min(y1, y3) - max(y2, y4)  # высота пересечения
                if width < height:
                    ball.direction = (360 - ball.direction) % 360
                    bounce.play()
                else:
                    ball.bounce(0)
                score += 1
            else:
                hitted1 = deadblocks[0]
                hitted2 = deadblocks[1]
                hitted_left = min(hitted1.rect.left, hitted2.rect.left)
                hitted_top = min(hitted1.rect.top, hitted2.rect.top)
                if hitted1.rect.left == hitted2.rect.left:
                    hitted_width = 23
                    hitted_height = 32
                else:
                    hitted_width = 48
                    hitted_height = 15
                hitted = pygame.Rect(hitted_left, hitted_top, hitted_width, hitted_height)
                x1, y1 = ball.rect.bottomleft
                x2, y2 = ball.rect.topright
                x3, y3 = hitted.bottomleft
                x4, y4 = hitted.topright
                width = min(x2, x4) - max(x1, x3)  # ширина пересечения
                height = min(y1, y3) - max(y2, y4)  # высота пересечения
                if width < height:
                    ball.direction = (360 - ball.direction) % 360
                    bounce.play()
                else:
                    ball.bounce(0)
                score += len(deadblocks)

            if len(blocks) == 0:  # Игрок сбил все блоки
                result = "Victory"
                whoosh.play()
                pygame.mixer.music.stop()
                game_over = True
                if nrow < 10:
                    nrow += 1
                    startballpos += block_height

        # Анимация мячика и ракетки
        if framecount == fps:
            ballframe += 1
            playerframe += 1
            framecount = 1
        if framecount % (fps // 6) == 0:
            ballframe += 1
            playerframe += 1
        if ballframe == 9:
            ballframe = 1
        if playerframe == 14:
            playerframe = 1
        if theme == "DARK":
            ball.image = pygame.image.load(os.path.join("images",
                                                        "ball",
                                                        "dark_theme",
                                                        f"ballframe{ballframe}.png"))
            player.image = pygame.image.load(os.path.join("images",
                                                          "player",
                                                          "dark_theme",
                                                          f"playerframe{playerframe}.png"))
        else:
            ball.image = pygame.image.load(os.path.join("images",
                                                        "ball",
                                                        "light_theme",
                                                        f"ballframe{ballframe}.png"))
            player.image = pygame.image.load(os.path.join("images",
                                                          "player",
                                                          "light_theme",
                                                          f"playerframe{playerframe}.png"))
        framecount += 1

        if speedup:
            screen.blit(xtext, xpos)
        allsprites.draw(screen)
        pygame.display.flip()
        start = False
