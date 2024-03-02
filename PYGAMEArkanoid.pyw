import math
import os
import random
import sys
import pickle
import pygame
from pygame.locals import *

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
grey = (127, 127, 127)
red = (225, 0, 0)
green = (0, 255, 0)
colors = ["red", "orange", "yellow", "green", "lightblue", "blue", "purple"]  # Цвета блоков
theme = "DARK"

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
os.environ["SDL_VIDEO_CENTERED"] = "1"
hints = ["even more ways to move the paddle", "try harder", "watch out", "press AltF4", "time to think",
         "do you have a strategy?", "chill out", "hurry up!", "press W", "press A", "press S", "press D",
         "press F", "press Esc", "don't press T", "press X", "blocks are falling", "listen to the music",
         "RAINBOW!", "don't play too much", "WASD, arrows and mouse", "no bugs at all", "what is your favourite song?",
         "...", "Arkanoid", "inspired by Taito", "1986", "what is your best score?"]
pygame.display.set_caption(f"Arkanoid: {random.choice(hints)}")  # В заголовке окна пишется случайная фраза
icon = pygame.Surface((10, 10))
pygame.display.set_icon(icon)
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
clock = pygame.time.Clock()
fps = 90  # 90 кадров в секунду
developer = "@super_nuke"
score = 0
volume = 100
difference = 0
selected = 0

# Шрифты
font = pygame.font.SysFont("Courier", 45, bold=True)
mediumfont = pygame.font.SysFont("Courier", 36, bold=True)
smallfont = pygame.font.SysFont("Courier", 35, bold=True)

# Звуки
whoosh = pygame.mixer.Sound(os.path.join("audio", "sounds", "introwhoosh.wav"))
bounce = pygame.mixer.Sound(os.path.join("audio", "sounds", "bounce.wav"))
music_themes = [1, 2, 3, 4, 5]

start = False
paused = False
settingsopened = False
extsettingsopened = False
advancesopened = False
playersopened = False
gitopened = False
resetopened = False


class Block(pygame.sprite.Sprite):
    """Класс для всех этих радужных блоков, которые нужно сбивать"""

    def __init__(self, color, x, y):  # Создание блока
        super().__init__()
        self.image = pygame.image.load(os.path.join("images", "blocks",
                                                    f"{color}block.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ball(pygame.sprite.Sprite):
    """На самом деле это квадрат"""

    speed = 0
    x = 0
    y = 0
    directions = [120, 140, 160, 180, 200, 220, 240]
    direction = 0
    width = 20
    height = 20

    def __init__(self):  # Создание мячика
        super().__init__()
        if theme == "DARK":
            self.image = pygame.image.load(os.path.join("images", "ball", "dark_theme",
                                                        "ballframe1.png"))
        else:
            self.image = pygame.image.load(os.path.join("images", "ball", "light_theme",
                                                        "ballframe1.png"))
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

    def bounce(self, d):  # Горизонтальный отскок мячика
        self.direction = (180 - self.direction) % 360
        self.direction -= d
        bounce.play()

    def vertical_bounce(self):  # Вертикальный отскок мячика
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
            self.bounce(0)
            self.y = 1
        if self.x <= 0:
            self.vertical_bounce()
            self.x = 1
        if self.x > self.screenwidth - self.width:
            self.vertical_bounce()
            self.x = self.screenwidth - self.width - 1
        if self.y > 600:
            return True
        else:
            return False


class Player(pygame.sprite.Sprite):
    """Плеер - дальше. Это Ракетка."""

    def __init__(self):  # Создание ракетки
        super().__init__()
        self.width = 100
        self.height = 15
        if theme == "DARK":
            self.image = pygame.image.load(os.path.join("images", "player", "dark_theme",
                                                        "playerframe1.png"))
        else:
            self.image = pygame.image.load(os.path.join("images", "player", "light_theme",
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
            self.rect.x = get_mouse_x()
            if self.rect.x > self.screenwidth - self.width:
                self.rect.x = self.screenwidth - self.width


# Открытие бинарного файла и чтение данных
f = open("highscore.dat", "rb")
try:
    players = pickle.load(f)
except EOFError:
    players = {"Player1": [0, 0]}
f.close()
if "Player1" in players.keys():
    if len(players["Player1"]) == 2:
        highscore = players["Player1"][0]
        highlevel = players["Player1"][1]
    else:
        highscore = 0
        highlevel = 0
        f.close()
        f = open("highscore.dat", "wb")
        players = {"Player1": [0, 0]}
        pickle.dump(players, f, True)
else:
    highscore = 0
    highlevel = 0
    f.close()
    f = open("highscore.dat", "wb")
    players = {"Player1": [0, 0]}
    pickle.dump(players, f, True)
f.close()

fog = pygame.Surface((800, 600))  # Затемняющая поверхность

# Текстовые индикаторы и кнопки
xtext = smallfont.render("X", True, white)
sptext = smallfont.render(f"{score}", True, white)
hscoretext = smallfont.render(f"Best score: {highscore}", True, white)
item1 = smallfont.render("resume (Esc)", True, white)
item2 = smallfont.render("new game (N)", True, white)
item3 = smallfont.render("settings (S)", True, white)
item4 = smallfont.render("exit (AltF4)", True, white)
item5 = smallfont.render("-", True, white)
item6 = smallfont.render("+", True, white)
item7 = smallfont.render(f"{volume}", True, white)
xpos = xtext.get_rect(centerx=775, top=5)
sppos = sptext.get_rect(left=5, top=5)
hscorepos = hscoretext.get_rect(left=10, top=560)
item1pos = item1.get_rect(centerx=400, top=310)
item2pos = item2.get_rect(centerx=400, top=350)
item3pos = item3.get_rect(centerx=400, top=390)
item4pos = item4.get_rect(centerx=400, top=430)
item5pos = item5.get_rect(centerx=431, top=350)
item6pos = item6.get_rect(centerx=515, top=350)
item7pos = item7.get_rect(centerx=473, top=350)

player = Player()  # Создание ракетки
ball = Ball()  # Создание мячика
startballpos = 180  # Начальная ордината мячика

# Добавление спрайтов в группы
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
balls.add(ball)
allsprites = pygame.sprite.Group()
allsprites.add(player)
allsprites.add(ball)


def close_arkanoid():  # Выход из игры
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


def f_write_score():  # Запись данных в бинарный файл и их чтение
    global f, players, score, highscore, level, highlevel
    f = open("highscore.dat", "rb")
    try:
        players = pickle.load(f)
    except EOFError:
        players = {"Player1": [0, 0]}
    f.close()
    if "Player1" in players.keys():
        if len(players["Player1"]) == 2:
            highscore = players["Player1"][0]
            highlevel = players["Player1"][1]
        else:
            highscore = 0
            highlevel = 0
            f.close()
            f = open("highscore.dat", "wb")
            players = {"Player1": [0, 0]}
            pickle.dump(players, f, True)
    else:
        highscore = 0
        highlevel = 0
        f.close()
        f = open("highscore.dat", "wb")
        players = {"Player1": [0, 0]}
        pickle.dump(players, f, True)
    f.close()
    if score > int(highscore):
        f = open("highscore.dat", "wb")
        players = {"Player1": [score, level]}
        pickle.dump(players, f, True)
        f.close()


def clear_items():  # Снятие выделения с элементов интерфейса
    global item1, item2, item3, item4, item5, item6, item7
    if theme == "DARK":
        if settingsopened:
            item1 = smallfont.render("< back (Esc)", True, white)
            item2 = smallfont.render("volume", True, white)
            item3 = smallfont.render("players (F5)", True, white)
            item4 = smallfont.render("more (Shift)", True, white)
            item5 = smallfont.render("-", True, white)
            item6 = smallfont.render("+", True, white)
            item7 = smallfont.render(f"{volume}", True, white)
        elif extsettingsopened:
            item1 = smallfont.render("< back (Esc)", True, white)
            item2 = smallfont.render("advances (A)", True, white)
            item3 = smallfont.render("github (F10)", True, white)
            item4 = smallfont.render("reset (AltR)", True, white)
        elif advancesopened:
            item1 = smallfont.render("coming soon!", True, white)
            item2 = smallfont.render("            ", True, white)
            item3 = smallfont.render("            ", True, white)
            item4 = smallfont.render("            ", True, white)
        elif playersopened:
            item1 = smallfont.render("coming soon!", True, white)
            item2 = smallfont.render("            ", True, white)
            item3 = smallfont.render("            ", True, white)
            item4 = smallfont.render("            ", True, white)
        elif gitopened:
            item1 = smallfont.render("coming soon!", True, white)
            item2 = smallfont.render("            ", True, white)
            item3 = smallfont.render("            ", True, white)
            item4 = smallfont.render("            ", True, white)
        elif resetopened:
            item1 = smallfont.render("coming soon!", True, white)
            item2 = smallfont.render("            ", True, white)
            item3 = smallfont.render("            ", True, white)
            item4 = smallfont.render("            ", True, white)
        else:
            item1 = smallfont.render("resume (Esc)", True, white)
            item2 = smallfont.render("new game (N)", True, white)
            item3 = smallfont.render("settings (S)", True, white)
            item4 = smallfont.render("exit (AltF4)", True, white)
    else:
        if settingsopened:
            item1 = smallfont.render("< back (Esc)", True, black)
            item2 = smallfont.render("volume", True, black)
            item3 = smallfont.render("players (F5)", True, black)
            item4 = smallfont.render("more (Shift)", True, black)
            item5 = smallfont.render("-", True, black)
            item6 = smallfont.render("+", True, black)
            item7 = smallfont.render(f"{volume}", True, black)
        elif extsettingsopened:
            item1 = smallfont.render("< back (Esc)", True, black)
            item2 = smallfont.render("advances (A)", True, black)
            item3 = smallfont.render("github (F10)", True, black)
            item4 = smallfont.render("reset (AltR)", True, black)
        elif advancesopened:
            item1 = smallfont.render("coming soon!", True, black)
            item2 = smallfont.render("            ", True, black)
            item3 = smallfont.render("            ", True, black)
            item4 = smallfont.render("            ", True, black)
        elif playersopened:
            item1 = smallfont.render("coming soon!", True, black)
            item2 = smallfont.render("            ", True, black)
            item3 = smallfont.render("            ", True, black)
            item4 = smallfont.render("            ", True, black)
        elif gitopened:
            item1 = smallfont.render("coming soon!", True, black)
            item2 = smallfont.render("            ", True, black)
            item3 = smallfont.render("            ", True, black)
            item4 = smallfont.render("            ", True, black)
        elif resetopened:
            item1 = smallfont.render("coming soon!", True, black)
            item2 = smallfont.render("            ", True, black)
            item3 = smallfont.render("            ", True, black)
            item4 = smallfont.render("            ", True, black)
        else:
            item1 = smallfont.render("resume (Esc)", True, black)
            item2 = smallfont.render("new game (N)", True, black)
            item3 = smallfont.render("settings (S)", True, black)
            item4 = smallfont.render("exit (AltF4)", True, black)


def center_items():  # Возвращение сдвинувшихся элементов интерфейса на исходные позиции
    global item1pos, item2pos, item3pos, item4pos, item5pos, item6pos, item7pos
    item1pos = item1.get_rect(centerx=400, top=310)
    if settingsopened:
        item2pos = item2.get_rect(centerx=337, top=350)
    else:
        item2pos = item2.get_rect(centerx=400, top=350)
    item3pos = item3.get_rect(centerx=400, top=390)
    item4pos = item4.get_rect(centerx=400, top=430)
    item5pos = item5.get_rect(centerx=431, top=350)
    item6pos = item6.get_rect(centerx=515, top=350)
    item7pos = item7.get_rect(centerx=473, top=350)


def pause():  # Большая функция, отвечающая за паузу
    global event,       \
        paused,         \
        selected,       \
        settingsopened, \
        game_over,      \
        result,         \
        nextlevel,      \
        score,          \
        allsprites,     \
        blocks,         \
        nrow,           \
        level,          \
        theme,          \
        xtext,          \
        sptext,         \
        hscoretext,     \
        item1,          \
        item2,          \
        item3,          \
        item4
    while paused:
        if theme == "DARK":
            xtext = smallfont.render("X", True, white)
            sptext = smallfont.render("||", True, white)
            hscoretext = smallfont.render(f"Best score: {highscore}", True, white)
            ball.image = pygame.image.load(os.path.join("images", "ball", "dark_theme",
                                                        f"ballframe{ballframe}.png"))
            player.image = pygame.image.load(os.path.join("images", "player", "dark_theme",
                                                          f"playerframe{playerframe}.png"))
        else:
            xtext = smallfont.render("X", True, black)
            sptext = smallfont.render("||", True, black)
            hscoretext = smallfont.render(f"Best score: {highscore}", True, black)
            ball.image = pygame.image.load(os.path.join("images", "ball", "light_theme",
                                                        f"ballframe{ballframe}.png"))
            player.image = pygame.image.load(os.path.join("images", "player", "light_theme",
                                                          f"playerframe{playerframe}.png"))
        if speedup:
            screen.blit(xtext, xpos)
        fog.set_alpha(200)
        if theme == "DARK":
            screen.fill(black)
            fog.fill(black)
        else:
            screen.fill(white)
            fog.fill(white)
        allsprites.draw(screen)
        screen.blit(fog, (0, 0))
        screen.blit(sptext, sppos)
        screen.blit(hscoretext, hscorepos)
        screen.blit(item1, item1pos)
        screen.blit(item2, item2pos)
        screen.blit(item3, item3pos)
        screen.blit(item4, item4pos)

        for event in pygame.event.get():  # Проверка событий
            if event.type == QUIT:
                event.key = None
                close_arkanoid()
            if event.type == KEYDOWN:
                if event.mod == KMOD_ALT and event.key == K_F4:
                    event.key = None
                    close_arkanoid()
                if event.key == K_t:
                    if theme == "LIGHT":
                        theme = "DARK"
                    else:
                        theme = "LIGHT"
                    event.key = None
                if event.key == K_ESCAPE:
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
                    pygame.mixer.music.unpause()
                    paused = False
                    event.key = None
                if event.key == K_n:
                    if theme == "DARK":
                        screen.fill(black)
                    else:
                        screen.fill(white)
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.queue(load_theme())
                    paused = False
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
                    event.key = None
                if event.key == K_s:
                    settingsopened = True
                    clear_items()
                    center_items()
                    event.key = None
                    settings()
                if event.key == K_DOWN:
                    if selected == 0 or selected == 4:
                        pygame.mouse.set_pos(item1pos.center)
                    elif selected == 1:
                        pygame.mouse.set_pos(item2pos.center)
                    elif selected == 2:
                        pygame.mouse.set_pos(item3pos.center)
                    elif selected == 3:
                        pygame.mouse.set_pos(item4pos.center)
                    event.key = None
                if event.key == K_UP:
                    if selected == 0 or selected == 1:
                        pygame.mouse.set_pos(item4pos.center)
                    elif selected == 2:
                        pygame.mouse.set_pos(item1pos.center)
                    elif selected == 3:
                        pygame.mouse.set_pos(item2pos.center)
                    elif selected == 4:
                        pygame.mouse.set_pos(item3pos.center)
                    event.key = None
            if item1pos.left <= get_mouse_x() <= item1pos.right and \
                    item1pos.top <= get_mouse_y() <= item1pos.bottom:
                clear_items()
                item1 = mediumfont.render("resume (Esc)", True, grey)
                center_items()
                selected = 1
                if event.type == MOUSEBUTTONUP and event.button == 1 or event.type == KEYDOWN and event.key == K_SPACE:
                    event.button = None
                    event.key = None
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
                    pygame.mixer.music.unpause()
                    if pygame.mixer.music.get_endevent():
                        pygame.mixer.music.queue(load_theme())
                    paused = False

            elif item2pos.left <= get_mouse_x() <= item2pos.right and \
                    item2pos.top <= get_mouse_y() <= item2pos.bottom:
                clear_items()
                item2 = mediumfont.render("new game (N)", True, grey)
                center_items()
                selected = 2
                if event.type == MOUSEBUTTONUP and event.button == 1 or event.type == KEYDOWN and event.key == K_SPACE:
                    event.button = None
                    event.key = None
                    if theme == "DARK":
                        screen.fill(black)
                    else:
                        screen.fill(white)
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.queue(load_theme())
                    paused = False
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

            elif item3pos.left <= get_mouse_x() <= item3pos.right and \
                    item3pos.top <= get_mouse_y() <= item3pos.bottom:
                clear_items()
                item3 = mediumfont.render("settings (S)", True, grey)
                center_items()
                selected = 3
                if event.type == MOUSEBUTTONUP and event.button == 1 or event.type == KEYDOWN and event.key == K_SPACE:
                    event.button = None
                    event.key = None
                    settingsopened = True
                    clear_items()
                    center_items()
                    settings()

            elif item4pos.left <= get_mouse_x() <= item4pos.right and \
                    item4pos.top <= get_mouse_y() <= item4pos.bottom:
                clear_items()
                item4 = mediumfont.render("exit (AltF4)", True, grey)
                center_items()
                selected = 4
                if event.type == MOUSEBUTTONUP and event.button == 1 or event.type == KEYDOWN and event.key == K_SPACE:
                    event.button = None
                    event.key = None
                    close_arkanoid()

            else:
                clear_items()
                center_items()
                selected = 0

        pygame.display.flip()
        clock.tick(fps)


def settings():  # Большая функция, отвечающая за настройки
    global event,       \
        settingsopened, \
        playersopened,  \
        selected,       \
        theme,          \
        volume,         \
        xtext,          \
        sptext,         \
        hscoretext,     \
        item1,          \
        item2,          \
        item3,          \
        item4,          \
        item5,          \
        item6,          \
        extsettingsopened
    while settingsopened:
        if speedup:
            screen.blit(xtext, xpos)
        fog.set_alpha(200)
        if theme == "DARK":
            screen.fill(black)
            fog.fill(black)
            ball.image = pygame.image.load(os.path.join("images", "ball", "dark_theme",
                                                        f"ballframe{ballframe}.png"))
            player.image = pygame.image.load(os.path.join("images", "player", "dark_theme",
                                                          f"playerframe{playerframe}.png"))
        else:
            screen.fill(white)
            fog.fill(white)
            ball.image = pygame.image.load(os.path.join("images", "ball", "light_theme",
                                                        f"ballframe{ballframe}.png"))
            player.image = pygame.image.load(os.path.join("images", "player", "light_theme",
                                                          f"playerframe{playerframe}.png"))
        allsprites.draw(screen)
        screen.blit(fog, (0, 0))
        screen.blit(sptext, sppos)
        screen.blit(item1, item1pos)
        screen.blit(item2, item2pos)
        screen.blit(item3, item3pos)
        screen.blit(item4, item4pos)
        screen.blit(item5, item5pos)
        screen.blit(item6, item6pos)
        screen.blit(item7, item7pos)
        for event in pygame.event.get():  # Проверка событий
            if event.type == QUIT:
                event.key = None
                close_arkanoid()
            if event.type == KEYDOWN:
                if event.mod == KMOD_ALT and event.key == K_F4:
                    event.key = None
                    close_arkanoid()
                if event.key == K_t:
                    if theme == "LIGHT":
                        theme = "DARK"
                    else:
                        theme = "LIGHT"
                    event.key = None
                if event.key == K_ESCAPE:
                    settingsopened = False
                    event.key = None
                    clear_items()
                    center_items()
                if event.key == K_RSHIFT or event.key == K_LSHIFT:
                    event.key = None
                    settingsopened = False
                    extsettingsopened = True
                    clear_items()
                    center_items()
                    ext_settings()
                if event.key == K_F5:
                    settingsopened = False
                    playersopened = True
                    clear_items()
                    center_items()
                    event.key = None
                    displayers()
                if event.key == K_MINUS or event.key == K_KP_MINUS:
                    if volume > 0:
                        volume -= 5
                        pygame.mixer.music.set_volume(volume / 100)
                    event.key = None
                if event.key == K_EQUALS or event.key == K_KP_PLUS:
                    if volume < 100:
                        volume += 5
                    event.key = None
                if event.key == K_DOWN:
                    if selected == 0 or selected == 4:
                        pygame.mouse.set_pos(item1pos.center)
                    elif selected == 1:
                        pygame.mouse.set_pos(item5pos.center)
                    elif selected == 3:
                        pygame.mouse.set_pos(item4pos.center)
                    elif selected == 5:
                        pygame.mouse.set_pos(item6pos.center)
                    elif selected == 6:
                        pygame.mouse.set_pos(item3pos.center)
                    event.key = None
                if event.key == K_UP:
                    if selected == 0 or selected == 1:
                        pygame.mouse.set_pos(item4pos.center)
                    elif selected == 3:
                        pygame.mouse.set_pos(item6pos.center)
                    elif selected == 4:
                        pygame.mouse.set_pos(item3pos.center)
                    elif selected == 5:
                        pygame.mouse.set_pos(item1pos.center)
                    elif selected == 6:
                        pygame.mouse.set_pos(item5pos.center)
                    event.key = None
                if event.key == K_SPACE:
                    if selected == 1:
                        settingsopened = False
                        clear_items()
                        center_items()
                    elif selected == 3:
                        settingsopened = False
                        playersopened = True
                        clear_items()
                        center_items()
                        displayers()
                    elif selected == 4:
                        settingsopened = False
                        extsettingsopened = True
                        clear_items()
                        center_items()
                        ext_settings()
                    elif selected == 5:
                        if volume > 0:
                            volume -= 5
                            pygame.mixer.music.set_volume(volume / 100)
                    elif selected == 6:
                        if volume < 100:
                            volume += 5
                            pygame.mixer.music.set_volume(volume / 100)
                    event.key = None

        if item1pos.left <= get_mouse_x() <= item1pos.right and \
                item1pos.top <= get_mouse_y() <= item1pos.bottom:
            clear_items()
            item1 = mediumfont.render("< back (Esc)", True, grey)
            center_items()
            selected = 1
            if event.type == MOUSEBUTTONUP and event.button == 1:
                event.key = None
                settingsopened = False
                clear_items()
                center_items()
        elif item3pos.left <= get_mouse_x() <= item3pos.right and \
                item3pos.top <= get_mouse_y() <= item3pos.bottom:
            clear_items()
            item3 = mediumfont.render("players (F5)", True, grey)
            center_items()
            selected = 3
            if event.type == MOUSEBUTTONUP and event.button == 1:
                event.key = None
                settingsopened = False
                playersopened = True
                clear_items()
                center_items()
                displayers()
        elif item4pos.left <= get_mouse_x() <= item4pos.right and \
                item4pos.top <= get_mouse_y() <= item4pos.bottom:
            clear_items()
            item4 = mediumfont.render("more (Shift)", True, grey)
            center_items()
            selected = 4
            if event.type == MOUSEBUTTONUP and event.button == 1 or event.type == KEYDOWN and event.key == K_SPACE:
                event.button = None
                event.key = None
                settingsopened = False
                extsettingsopened = True
                clear_items()
                center_items()
                ext_settings()
        elif item5pos.left <= get_mouse_x() <= item5pos.right and \
                item5pos.top <= get_mouse_y() <= item5pos.bottom:
            clear_items()
            item5 = smallfont.render("-", True, grey)
            center_items()
            selected = 5
            if event.type == MOUSEBUTTONUP and event.button == 1 or event.type == KEYDOWN and event.key == K_SPACE:
                event.button = None
                event.key = None
                if volume > 0:
                    volume -= 5
                    event.button = 0
                    pygame.mixer.music.set_volume(volume / 100)
        elif item6pos.left <= get_mouse_x() <= item6pos.right and \
                item6pos.top <= get_mouse_y() <= item6pos.bottom:
            clear_items()
            item6 = smallfont.render("+", True, grey)
            center_items()
            selected = 6
            if event.type == MOUSEBUTTONUP and event.button == 1 or event.type == KEYDOWN and event.key == K_SPACE:
                event.button = None
                event.key = None
                if volume < 100:
                    volume += 5
                    event.button = 0
                    pygame.mixer.music.set_volume(volume / 100)
        else:
            clear_items()
            center_items()

        pygame.display.flip()
        clock.tick(fps)


def displayers():  # Список игроков
    global event,       \
        settingsopened, \
        playersopened,  \
        selected,       \
        theme,          \
        xtext,          \
        sptext,         \
        hscoretext,     \
        item1,          \
        item2,          \
        item3,          \
        item4
    while playersopened:
        if speedup:
            screen.blit(xtext, xpos)
        fog.set_alpha(200)
        if theme == "DARK":
            fog.fill(black)
            ball.image = pygame.image.load(os.path.join("images", "ball", "dark_theme",
                                                        f"ballframe{ballframe}.png"))
            player.image = pygame.image.load(os.path.join("images", "player", "dark_theme",
                                                          f"playerframe{playerframe}.png"))
        else:
            fog.fill(white)
            ball.image = pygame.image.load(os.path.join("images", "ball", "light_theme",
                                                        f"ballframe{ballframe}.png"))
            player.image = pygame.image.load(os.path.join("images", "player", "light_theme",
                                                          f"playerframe{playerframe}.png"))
        allsprites.draw(screen)
        screen.blit(fog, (0, 0))
        screen.blit(sptext, sppos)
        screen.blit(item1, item1pos)
        screen.blit(item2, item2pos)
        screen.blit(item3, item3pos)
        screen.blit(item4, item4pos)
        for event in pygame.event.get():  # Проверка событий
            if event.type == QUIT:
                event.key = None
                close_arkanoid()
            if event.type == KEYDOWN:
                if event.mod == KMOD_ALT and event.key == K_F4:
                    close_arkanoid()
                if event.key == K_t:
                    if theme == "LIGHT":
                        theme = "DARK"
                    else:
                        theme = "LIGHT"
                    event.key = None
                if event.key == K_ESCAPE:
                    playersopened = False
                    settingsopened = True
                    event.key = None
                    clear_items()
                    center_items()
        if item1pos.left <= get_mouse_x() <= item1pos.right and \
                item1pos.top <= get_mouse_y() <= item1pos.bottom:
            clear_items()
            item1 = mediumfont.render("< back (Esc)", True, grey)
            center_items()
            selected = 1
            if event.type == MOUSEBUTTONUP and event.button == 1:
                event.button = None
                playersopened = False
                settingsopened = True
                clear_items()
                center_items()
        else:
            clear_items()
            center_items()

        pygame.display.flip()
        clock.tick(fps)


def advances():
    global event,       \
        advancesopened, \
        selected,       \
        theme,          \
        xtext,          \
        sptext,         \
        hscoretext,     \
        item1,          \
        item2,          \
        item3,          \
        item4,          \
        extsettingsopened
    while advancesopened:
        if speedup:
            screen.blit(xtext, xpos)
        fog.set_alpha(200)
        if theme == "DARK":
            fog.fill(black)
            ball.image = pygame.image.load(os.path.join("images", "ball", "dark_theme",
                                                        f"ballframe{ballframe}.png"))
            player.image = pygame.image.load(os.path.join("images", "player", "dark_theme",
                                                          f"playerframe{playerframe}.png"))
        else:
            fog.fill(white)
            ball.image = pygame.image.load(os.path.join("images", "ball", "light_theme",
                                                        f"ballframe{ballframe}.png"))
            player.image = pygame.image.load(os.path.join("images", "player", "light_theme",
                                                          f"playerframe{playerframe}.png"))
        allsprites.draw(screen)
        screen.blit(fog, (0, 0))
        screen.blit(sptext, sppos)
        screen.blit(item1, item1pos)
        screen.blit(item2, item2pos)
        screen.blit(item3, item3pos)
        screen.blit(item4, item4pos)
        for event in pygame.event.get():  # Проверка событий
            if event.type == QUIT:
                event.key = None
                close_arkanoid()
            if event.type == KEYDOWN:
                if event.mod == KMOD_ALT and event.key == K_F4:
                    close_arkanoid()
                if event.key == K_t:
                    if theme == "LIGHT":
                        theme = "DARK"
                    else:
                        theme = "LIGHT"
                    event.key = None
                if event.key == K_ESCAPE:
                    advancesopened = False
                    extsettingsopened = True
                    event.key = None
                    clear_items()
                    center_items()
        if item1pos.left <= get_mouse_x() <= item1pos.right and \
                item1pos.top <= get_mouse_y() <= item1pos.bottom:
            clear_items()
            item1 = mediumfont.render("< back (Esc)", True, grey)
            center_items()
            selected = 1
            if event.type == MOUSEBUTTONUP and event.button == 1:
                event.button = None
                advancesopened = False
                extsettingsopened = True
                clear_items()
                center_items()
        else:
            clear_items()
            center_items()

        pygame.display.flip()
        clock.tick(fps)


def opengit():
    global event,       \
        gitopened,      \
        selected,       \
        theme,          \
        xtext,          \
        sptext,         \
        hscoretext,     \
        item1,          \
        item2,          \
        item3,          \
        item4,          \
        extsettingsopened
    while gitopened:
        if speedup:
            screen.blit(xtext, xpos)
        fog.set_alpha(200)
        if theme == "DARK":
            fog.fill(black)
            ball.image = pygame.image.load(os.path.join("images", "ball", "dark_theme",
                                                        f"ballframe{ballframe}.png"))
            player.image = pygame.image.load(os.path.join("images", "player", "dark_theme",
                                                          f"playerframe{playerframe}.png"))
        else:
            fog.fill(white)
            ball.image = pygame.image.load(os.path.join("images", "ball", "light_theme",
                                                        f"ballframe{ballframe}.png"))
            player.image = pygame.image.load(os.path.join("images", "player", "light_theme",
                                                          f"playerframe{playerframe}.png"))
        allsprites.draw(screen)
        screen.blit(fog, (0, 0))
        screen.blit(sptext, sppos)
        screen.blit(item1, item1pos)
        screen.blit(item2, item2pos)
        screen.blit(item3, item3pos)
        screen.blit(item4, item4pos)
        for event in pygame.event.get():  # Проверка событий
            if event.type == QUIT:
                event.key = None
                close_arkanoid()
            if event.type == KEYDOWN:
                if event.mod == KMOD_ALT and event.key == K_F4:
                    close_arkanoid()
                if event.key == K_t:
                    if theme == "LIGHT":
                        theme = "DARK"
                    else:
                        theme = "LIGHT"
                    event.key = None
                if event.key == K_ESCAPE:
                    gitopened = False
                    extsettingsopened = True
                    event.key = None
                    clear_items()
                    center_items()
        if item1pos.left <= get_mouse_x() <= item1pos.right and \
                item1pos.top <= get_mouse_y() <= item1pos.bottom:
            clear_items()
            item1 = mediumfont.render("< back (Esc)", True, grey)
            center_items()
            selected = 1
            if event.type == MOUSEBUTTONUP and event.button == 1:
                event.button = None
                gitopened = False
                extsettingsopened = True
                clear_items()
                center_items()
        else:
            clear_items()
            center_items()

        pygame.display.flip()
        clock.tick(fps)


def reset():
    global event,       \
        resetopened,    \
        selected,       \
        theme,          \
        xtext,          \
        sptext,         \
        hscoretext,     \
        item1,          \
        item2,          \
        item3,          \
        item4,          \
        extsettingsopened
    while resetopened:
        if speedup:
            screen.blit(xtext, xpos)
        fog.set_alpha(200)
        if theme == "DARK":
            fog.fill(black)
            ball.image = pygame.image.load(os.path.join("images", "ball", "dark_theme",
                                                        f"ballframe{ballframe}.png"))
            player.image = pygame.image.load(os.path.join("images", "player", "dark_theme",
                                                          f"playerframe{playerframe}.png"))
        else:
            fog.fill(white)
            ball.image = pygame.image.load(os.path.join("images", "ball", "light_theme",
                                                        f"ballframe{ballframe}.png"))
            player.image = pygame.image.load(os.path.join("images", "player", "light_theme",
                                                          f"playerframe{playerframe}.png"))
        allsprites.draw(screen)
        screen.blit(fog, (0, 0))
        screen.blit(sptext, sppos)
        screen.blit(item1, item1pos)
        screen.blit(item2, item2pos)
        screen.blit(item3, item3pos)
        screen.blit(item4, item4pos)
        for event in pygame.event.get():  # Проверка событий
            if event.type == QUIT:
                event.key = None
                close_arkanoid()
            if event.type == KEYDOWN:
                if event.mod == KMOD_ALT and event.key == K_F4:
                    close_arkanoid()
                if event.key == K_t:
                    if theme == "LIGHT":
                        theme = "DARK"
                    else:
                        theme = "LIGHT"
                    event.key = None
                if event.key == K_ESCAPE:
                    resetopened = False
                    extsettingsopened = True
                    event.key = None
                    clear_items()
                    center_items()
        if item1pos.left <= get_mouse_x() <= item1pos.right and \
                item1pos.top <= get_mouse_y() <= item1pos.bottom:
            clear_items()
            item1 = mediumfont.render("< back (Esc)", True, grey)
            center_items()
            selected = 1
            if event.type == MOUSEBUTTONUP and event.button == 1:
                event.button = None
                resetopened = False
                extsettingsopened = True
                clear_items()
                center_items()
        else:
            clear_items()
            center_items()

        pygame.display.flip()
        clock.tick(fps)


def ext_settings():  # Дополнительные настройки
    global event,       \
        settingsopened, \
        advancesopened, \
        gitopened,      \
        resetopened,    \
        selected,       \
        theme,          \
        volume,         \
        xtext,          \
        sptext,         \
        hscoretext,     \
        item1,          \
        item2,          \
        item3,          \
        item4,          \
        item5,          \
        item6,          \
        extsettingsopened
    while extsettingsopened:
        if speedup:
            screen.blit(xtext, xpos)
        fog.set_alpha(200)
        if theme == "DARK":
            fog.fill(black)
            ball.image = pygame.image.load(os.path.join("images", "ball", "dark_theme",
                                                        f"ballframe{ballframe}.png"))
            player.image = pygame.image.load(os.path.join("images", "player", "dark_theme",
                                                          f"playerframe{playerframe}.png"))
        else:
            fog.fill(white)
            ball.image = pygame.image.load(os.path.join("images", "ball", "light_theme",
                                                        f"ballframe{ballframe}.png"))
            player.image = pygame.image.load(os.path.join("images", "player", "light_theme",
                                                          f"playerframe{playerframe}.png"))
        allsprites.draw(screen)
        screen.blit(fog, (0, 0))
        screen.blit(sptext, sppos)
        screen.blit(item1, item1pos)
        screen.blit(item2, item2pos)
        screen.blit(item3, item3pos)
        screen.blit(item4, item4pos)
        for event in pygame.event.get():  # Проверка событий
            if event.type == QUIT:
                event.key = None
                close_arkanoid()
            if event.type == KEYDOWN:
                if event.mod == KMOD_ALT and event.key == K_F4:
                    close_arkanoid()
                    if event.key == K_r:
                        extsettingsopened = False
                        resetopened = True
                        event.key = None
                        clear_items()
                        center_items()
                        reset()
                    event.key = None
                if event.key == K_t:
                    if theme == "LIGHT":
                        theme = "DARK"
                    else:
                        theme = "LIGHT"
                    event.key = None
                if event.key == K_ESCAPE:
                    extsettingsopened = False
                    settingsopened = True
                    event.key = None
                    clear_items()
                    center_items()
                if event.key == K_a:
                    extsettingsopened = False
                    advancesopened = True
                    event.key = None
                    clear_items()
                    center_items()
                    advances()
                if event.key == K_F10:
                    extsettingsopened = False
                    gitopened = True
                    event.key = None
                    clear_items()
                    center_items()
                    opengit()
                if event.key == K_DOWN:
                    if selected == 0 or selected == 4:
                        pygame.mouse.set_pos(item1pos.center)
                    elif selected == 1:
                        pygame.mouse.set_pos(item2pos.center)
                    elif selected == 2:
                        pygame.mouse.set_pos(item3pos.center)
                    elif selected == 3:
                        pygame.mouse.set_pos(item4pos.center)
                    event.key = None
                if event.key == K_UP:
                    if selected == 0 or selected == 1:
                        pygame.mouse.set_pos(item4pos.center)
                    elif selected == 2:
                        pygame.mouse.set_pos(item1pos.center)
                    elif selected == 3:
                        pygame.mouse.set_pos(item2pos.center)
                    elif selected == 4:
                        pygame.mouse.set_pos(item3pos.center)
                    event.key = None
                if event.key == K_SPACE:
                    if selected == 1:
                        extsettingsopened = False
                        settingsopened = True
                        clear_items()
                        center_items()
                    elif selected == 2:
                        extsettingsopened = False
                        advancesopened = True
                        clear_items()
                        center_items()
                        advances()
                    elif selected == 3:
                        extsettingsopened = False
                        gitopened = True
                        event.key = None
                        clear_items()
                        center_items()
                        opengit()
                    elif selected == 4:
                        extsettingsopened = False
                        resetopened = True
                        event.key = None
                        clear_items()
                        center_items()
                        reset()
                    event.key = None
        if item1pos.left <= get_mouse_x() <= item1pos.right and \
                item1pos.top <= get_mouse_y() <= item1pos.bottom:
            clear_items()
            item1 = mediumfont.render("< back (Esc)", True, grey)
            center_items()
            selected = 1
            if event.type == MOUSEBUTTONUP and event.button == 1:
                event.button = None
                extsettingsopened = False
                settingsopened = True
                clear_items()
                center_items()
        elif item2pos.left <= get_mouse_x() <= item2pos.right and \
                item2pos.top <= get_mouse_y() <= item2pos.bottom:
            clear_items()
            item2 = mediumfont.render("advances (A)", True, grey)
            center_items()
            selected = 2
            if event.type == MOUSEBUTTONUP and event.button == 1:
                event.button = None
                extsettingsopened = False
                advancesopened = True
                clear_items()
                center_items()
                advances()
        elif item3pos.left <= get_mouse_x() <= item3pos.right and \
                item3pos.top <= get_mouse_y() <= item3pos.bottom:
            clear_items()
            item3 = mediumfont.render("github (F10)", True, grey)
            center_items()
            selected = 3
            if event.type == MOUSEBUTTONUP and event.button == 1:
                extsettingsopened = False
                gitopened = True
                event.key = None
                clear_items()
                center_items()
                opengit()
        elif item4pos.left <= get_mouse_x() <= item4pos.right and \
                item4pos.top <= get_mouse_y() <= item4pos.bottom:
            clear_items()
            item4 = mediumfont.render("reset (AltR)", True, grey)
            center_items()
            selected = 4
            if event.type == MOUSEBUTTONUP and event.button == 1:
                extsettingsopened = False
                resetopened = True
                event.key = None
                clear_items()
                center_items()
                reset()
        else:
            clear_items()
            center_items()

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
                    close_arkanoid()
                if event.type == MOUSEBUTTONDOWN:
                    start = True
                    break
                if event.type == KEYDOWN:
                    if event.mod == KMOD_ALT:
                        if event.key == K_F4:
                            close_arkanoid()
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
                    close_arkanoid()
                if event.type == MOUSEBUTTONDOWN:
                    start = True
                    break
                if event.type == KEYDOWN:
                    if event.mod == KMOD_ALT:
                        if event.key == K_F4:
                            close_arkanoid()
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

while developer == "@super_nuke":
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
                    close_arkanoid()
                if event.type == MOUSEBUTTONDOWN:
                    start = True
                    deadblocks.clear()
                    allsprites = pygame.sprite.Group()
                    allsprites.add(ball)
                    allsprites.add(player)
                    blocks = pygame.sprite.Group()
                    break
                if event.type == KEYDOWN:
                    if event.mod == KMOD_ALT:
                        if event.key == K_F4:
                            close_arkanoid()
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
                b.rect.y += random.randint(2, 3)

            clock.tick(fps)
            if theme == "DARK":
                screen.fill(black)
                player.image = pygame.image.load(os.path.join("images", "player", "dark_theme",
                                                              f"playerframe{playerframe}.png"))
            else:
                screen.fill(white)
                player.image = pygame.image.load(os.path.join("images", "player", "light_theme",
                                                              f"playerframe{playerframe}.png"))

            if not nextlevel:
                text1 = smallfont.render("Press any key to start new game", True, (i, i, i))
            else:
                text1 = smallfont.render("Press any key to start next level", True, (i, i, i))
            text1pos = text1.get_rect(centerx=background.get_width() / 2)
            text1pos.top = 450
            screen.blit(text1, text1pos)

            allsprites.draw(screen)

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
                    close_arkanoid()
                if event.type == MOUSEBUTTONDOWN:
                    start = True
                    deadblocks.clear()
                    allsprites = pygame.sprite.Group()
                    allsprites.add(ball)
                    allsprites.add(player)
                    blocks = pygame.sprite.Group()
                    break
                if event.type == KEYDOWN:
                    if event.mod == KMOD_ALT:
                        if event.key == K_F4:
                            close_arkanoid()
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
                    b.rect.y += random.randint(2, 3)

            clock.tick(fps)
            if theme == "DARK":
                screen.fill(black)
                player.image = pygame.image.load(os.path.join("images", "player", "dark_theme",
                                                              f"playerframe{playerframe}.png"))
            else:
                screen.fill(white)
                player.image = pygame.image.load(os.path.join("images", "player", "light_theme",
                                                              f"playerframe{playerframe}.png"))

            if not nextlevel:
                text1 = smallfont.render("Press any key to start new game", True, (i, i, i))
            else:
                text1 = smallfont.render("Press any key to start next level", True, (i, i, i))
            text1pos = text1.get_rect(centerx=background.get_width() / 2)
            text1pos.top = 450
            screen.blit(text1, text1pos)

            allsprites.draw(screen)

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
        f_write_score()
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
    levels = [["11111111111111111111111111111111",  # 1st level
               "11111111111111111111111111111111",
               "11111111111111111111111111111111",
               "11111111111111111111111111111111"],

              ["00101010101010101010101010101010",  # 2nd level
               "01010101010101010101010101010100",
               "00101010101010101010101010101010",
               "01010101010101010101010101010100",
               "00101010101010101010101010101010"],

              ["11111111111111111111111111111111",  # 3rd level
               "10000000000000000000000000000001",
               "10111111111111111111111111111101",
               "10111111111111111111111111111101",
               "10000000000000000000000000000001",
               "11111111111111111111111111111111"],

              ["11111111111111110011001100110011",  # 4th level
               "11111111111111110011001100110011",
               "11001100110011000011001100110011",
               "11001100110011000011001100110011",
               "11001100110011000011001100110011",
               "11001100110011001111111111111111",
               "11001100110011001111111111111111"],

              ["11001100110011001100110011001100",  # 5th level
               "11001100110011001100110011001100",
               "00110011001100110011001100110011",
               "00110011001100110011001100110011",
               "11001100110011001100110011001100",
               "11001100110011001100110011001100",
               "00110011001100110011001100110011",
               "00110011001100110011001100110011"],

              ["00001000001000001000001000001000",  # 6th level
               "10000010000010000010000010000010",
               "00100000100000100000100000100000",
               "00001000001000001000001000001000",
               "10000010000010000010000010000010",
               "00100000100000100000100000100000",
               "00001000001000001000001000001000",
               "00100000100000100000100000100000",
               "10000010000010000010000010000010"],

              ["01001001011010010110100101100010",  # 7th level
               "00101011101001010010010101001010",
               "11110010111001010101010110101010",
               "01010101000110110110100111111111",
               "01001011111111000100101010000111",
               "01010100110010110100100100100111",
               "10100100101101000101010101010110",
               "01011101001001011001100011101010",
               "00000011111011010100010111100111",
               "01010101010000000111111111011011"],

              ["01111111111111111111111111111110",  # 8th level
               "10000000000000000000000000000001",
               "10011111111111111111111111111001",
               "10100000000000000000000000000101",
               "10101111111111111111111111110101",
               "10100000000000000000000000000101",
               "10011111111111111111111111111001",
               "10000000000000000000000000000001",
               "01111111111111111111111111111110"]]

    if level <= 8:
        for row in range(len(levels[level-1])):  # Отрисовка блоков
            for column in range(ncolumn):
                if int(levels[level-1][row][column]):
                    block = Block(random.choice(colors), column * (block_width + 2) + 1, top)
                    blocks.add(block)
                    allsprites.add(block)
            top += block_height + 2
    else:
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
            sptext = smallfont.render(f"{score}", True, white)
        else:
            screen.fill(white)
            xtext = smallfont.render("X", True, black)
            sptext = smallfont.render(f"{score}", True, black)

        if pygame.mixer.music.get_endevent():
            pygame.mixer.music.queue(load_theme())

        for event in pygame.event.get():  # Проверка событий
            if event.type == QUIT:
                close_arkanoid()
            if event.type == KEYDOWN:
                if event.mod == KMOD_ALT:
                    if event.key == K_F4:
                        close_arkanoid()
                if event.key == K_t:
                    if theme == "LIGHT":
                        theme = "DARK"
                    else:
                        theme = "LIGHT"
                if event.key == K_ESCAPE:
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)
                    pygame.mixer.music.pause()
                    paused = True
                if event.key == K_x:
                    speedup = not speedup
                    if speedup:
                        currentspeed = ball.speed
                        ball.speed *= 2
                    else:
                        ball.speed = currentspeed
                if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_a or event.key == K_d:
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

        if paused:
            pause()

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
                ball.vertical_bounce()
            else:
                ball.y -= 5
                difference = player.rect.centerx - ball.rect.centerx
                if difference > 30:
                    difference = 30
                ball.bounce(difference)
                if 85 < ball.direction < 180:
                    ball.direction = 85
                elif 180 < ball.direction < 275:
                    ball.direction = 275
                ball.speed += 0.03
                if ball.direction < 0:
                    ball.direction += 360
                if ball.direction >= 360:
                    ball.direction -= 360

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
                    ball.vertical_bounce()
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
                    ball.vertical_bounce()
                else:
                    ball.bounce(0)
                score += len(deadblocks)
                if ball.direction < 0:
                    ball.direction += 360
                if ball.direction >= 360:
                    ball.direction -= 360

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
            ball.image = pygame.image.load(os.path.join("images", "ball", "dark_theme",
                                                        f"ballframe{ballframe}.png"))
            player.image = pygame.image.load(os.path.join("images", "player", "dark_theme",
                                                          f"playerframe{playerframe}.png"))
        else:
            ball.image = pygame.image.load(os.path.join("images", "ball", "light_theme",
                                                        f"ballframe{ballframe}.png"))
            player.image = pygame.image.load(os.path.join("images", "player",  "light_theme",
                                                          f"playerframe{playerframe}.png"))
        framecount += 1

        if speedup:
            screen.blit(xtext, xpos)
        screen.blit(sptext, sppos)
        allsprites.draw(screen)
        pygame.display.flip()
        start = False
