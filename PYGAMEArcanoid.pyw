import math
import os
import sys
import random
import pygame
from pygame.locals import *


class Block(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.image.load(f"images\\{color}block.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ball(pygame.sprite.Sprite):
    speed = 0
    x = 0
    y = 0
    directions = [60, 120, 240, 300]
    direction = 0
    width = 20
    height = 20

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images\\ball.png")
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

    def bounce(self, d):
        self.direction = (180 - self.direction) % 360
        self.direction -= d
        bounce.play()

    def update(self):
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
    def __init__(self):
        super().__init__()
        self.width = 100
        self.height = 15
        self.image = pygame.image.load("images\\player.png")
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        self.rect.x = random.randint(0, 725)
        self.rect.y = self.screenheight - self.height - 2

    def update(self):
        self.rect.x = get_mouse_x()
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width


black = (0, 0, 0)
green = (0, 255, 0)
lightgrey = (145, 145, 145)
red = (225, 0, 0)
white = (255, 255, 255)
colors = ["red", "orange", "yellow", "green", "lightblue", "blue", "purple"]
block_width = 23
block_height = 15
fps = 90

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Arcanoid")
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
font = pygame.font.SysFont('Courier', 45, bold=True)
mediumfont = pygame.font.SysFont('Courier', 36, bold=True)
smallfont = pygame.font.SysFont('Courier', 35, bold=True)
whoosh = pygame.mixer.Sound("audio\\introwhoosh.wav")
bounce = pygame.mixer.Sound("audio\\bounce.wav")
themes = [1, 2, 3, 4, 5]
background = pygame.Surface(screen.get_size())
player = Player()
ball = Ball()
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
allsprites = pygame.sprite.Group()
allsprites.add(player)
allsprites.add(ball)
balls.add(ball)
start = False
paused = False


def get_mouse_x():
    return pygame.mouse.get_pos()[0]


def get_mouse_y():
    return pygame.mouse.get_pos()[1]


def load_theme(mode, theme=1):
    loaded = ""
    if mode:
        theme = random.randint(1, 5)
    if theme == 1:
        pygame.mixer.music.load("audio\\Viscid_ErrorRate.mp3")
        loaded = "audio\\Viscid_ErrorRate.mp3"
    elif theme == 2:
        pygame.mixer.music.load("audio\\Viscid_Humdrum.mp3")
        loaded = "audio\\Viscid_Humdrum.mp3"
    elif theme == 3:
        pygame.mixer.music.load("audio\\Viscid_Ictus.mp3")
        loaded = "audio\\Viscid_Ictus.mp3"
    elif theme == 4:
        pygame.mixer.music.load("audio\\Viscid_Plunge.mp3")
        loaded = "audio\\Viscid_Plunge.mp3"
    elif theme == 5:
        pygame.mixer.music.load("audio\\Viscid_Zigzag.mp3")
        loaded = "audio\\Viscid_Zigzag.mp3"
    return loaded


def pausecheck():
    global event, paused, game_over, result
    while paused:
        pauseclose = False
        pausetext = smallfont.render("||", True, white)
        pausepos = pausetext.get_rect(centerx=25)
        pausepos.top = 5
        item1 = smallfont.render("resume (Esc)", True, white)
        item1pos = item1.get_rect(centerx=background.get_width() / 2)
        item1pos.top = 300
        item2 = smallfont.render("new game (N)", True, white)
        item2pos = item2.get_rect(centerx=background.get_width() / 2)
        item2pos.top = 350
        item3 = smallfont.render("exit (AltF4)", True, white)
        item3pos = item3.get_rect(centerx=background.get_width() / 2)
        item3pos.top = 400
        fog = pygame.Surface((800, 600))
        fog.fill(black)
        fog.set_alpha(200)
        allsprites.draw(screen)
        screen.blit(fog, (0, 0))
        screen.blit(pausetext, pausepos)
        screen.blit(item1, item1pos)
        screen.blit(item2, item2pos)
        screen.blit(item3, item3pos)
        selected = 0
        while not pauseclose:
            allsprites.draw(screen)
            screen.blit(fog, (0, 0))
            screen.blit(pausetext, pausepos)
            screen.blit(item1, item1pos)
            screen.blit(item2, item2pos)
            screen.blit(item3, item3pos)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_LALT or event.key == K_RALT:
                        if event.mod == KMOD_ALT:
                            if event.key == K_F4:
                                pygame.quit()
                                sys.exit()
                    if event.key == K_ESCAPE:
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)
                        pygame.mixer.music.set_volume(volume)
                        if pygame.mixer.music.get_endevent():
                            pygame.mixer.music.queue(load_theme(True))
                        paused = False
                        pauseclose = True
                    if event.key == K_n:
                        screen.fill(black)
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)
                        pygame.mixer.music.set_volume(volume)
                        pygame.mixer.music.stop()
                        pygame.mixer.music.queue(load_theme(True))
                        paused = False
                        pauseclose = True
                        result = None
                        game_over = True
                if event.type == pygame.MOUSEMOTION:
                    if item1pos.left <= get_mouse_x() <= item1pos.right and \
                            item1pos.top <= get_mouse_y() <= item1pos.bottom:
                        item1 = mediumfont.render("resume (Esc)", True, lightgrey)
                        item1pos = item1.get_rect(centerx=background.get_width() / 2)
                        item1pos.top = 300
                        item2 = smallfont.render("new game (N)", True, white)
                        item2pos = item2.get_rect(centerx=background.get_width() / 2)
                        item2pos.top = 350
                        item3 = smallfont.render("exit (AltF4)", True, white)
                        item3pos = item3.get_rect(centerx=background.get_width() / 2)
                        item3pos.top = 400
                        selected = 1
                    elif item2pos.left <= get_mouse_x() <= item2pos.right and \
                            item2pos.top <= get_mouse_y() <= item2pos.bottom:
                        item1 = smallfont.render("resume (Esc)", True, white)
                        item1pos = item1.get_rect(centerx=background.get_width() / 2)
                        item1pos.top = 300
                        item2 = mediumfont.render("new game (N)", True, lightgrey)
                        item2pos = item2.get_rect(centerx=background.get_width() / 2)
                        item2pos.top = 350
                        item3 = smallfont.render("exit (AltF4)", True, white)
                        item3pos = item3.get_rect(centerx=background.get_width() / 2)
                        item3pos.top = 400
                        selected = 2
                    elif item3pos.left <= get_mouse_x() <= item3pos.right and \
                            item3pos.top <= get_mouse_y() <= item3pos.bottom:
                        item1 = smallfont.render("resume (Esc)", True, white)
                        item1pos = item1.get_rect(centerx=background.get_width() / 2)
                        item1pos.top = 300
                        item2 = smallfont.render("new game (N)", True, white)
                        item2pos = item2.get_rect(centerx=background.get_width() / 2)
                        item2pos.top = 350
                        item3 = mediumfont.render("exit (AltF4)", True, lightgrey)
                        item3pos = item3.get_rect(centerx=background.get_width() / 2)
                        item3pos.top = 400
                        selected = 3
                    else:
                        item1 = smallfont.render("resume (Esc)", True, white)
                        item1pos = item1.get_rect(centerx=background.get_width() / 2)
                        item1pos.top = 300
                        item2 = smallfont.render("new game (N)", True, white)
                        item2pos = item2.get_rect(centerx=background.get_width() / 2)
                        item2pos.top = 350
                        item3 = smallfont.render("exit (AltF4)", True, white)
                        item3pos = item3.get_rect(centerx=background.get_width() / 2)
                        item3pos.top = 400
                if selected == 1:
                    if event.type == MOUSEBUTTONUP:
                        if item1pos.left <= get_mouse_x() <= item1pos.right and \
                                item1pos.top <= get_mouse_y() <= item1pos.bottom:
                            pygame.mouse.set_visible(False)
                            pygame.event.set_grab(True)
                            pygame.mixer.music.set_volume(volume)
                            if pygame.mixer.music.get_endevent():
                                pygame.mixer.music.queue(load_theme(True))
                            paused = False
                            pauseclose = True
                elif selected == 2:
                    if event.type == MOUSEBUTTONUP:
                        if item2pos.left <= get_mouse_x() <= item2pos.right and \
                                item2pos.top <= get_mouse_y() <= item2pos.bottom:
                            screen.fill(black)
                            pygame.mouse.set_visible(False)
                            pygame.event.set_grab(True)
                            pygame.mixer.music.set_volume(volume)
                            pygame.mixer.music.stop()
                            pygame.mixer.music.queue(load_theme(True))
                            paused = False
                            pauseclose = True
                            result = None
                            game_over = True
                elif selected == 3:
                    if event.type == MOUSEBUTTONUP:
                        if item3pos.left <= get_mouse_x() <= item3pos.right and \
                                item3pos.top <= get_mouse_y() <= item3pos.bottom:
                            pygame.quit()
                            sys.exit()
            pygame.display.flip()


def intro():
    global start, i, event
    whoosh.play()
    while not start:
        for i in range(0, 255, 2):
            text = smallfont.render("Press any key to start the game", True, (i, i, i))
            textpos = text.get_rect(centerx=background.get_width() / 2)
            textpos.top = 400
            for event in pygame.event.get():
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
                    else:
                        start = True
                        break
            if start:
                load_theme(True)
                pygame.mixer.music.queue(load_theme(True))
                pygame.mixer.music.play()
                break
            clock.tick(fps)
            screen.fill(black)
            screen.blit(text, textpos)
            pygame.display.flip()
        for i in range(255, 0, -2):
            text = smallfont.render("Press any key to start the game", True, (i, i, i))
            textpos = text.get_rect(centerx=background.get_width() / 2)
            textpos.top = 400
            for event in pygame.event.get():
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
                    else:
                        start = True
                        break
            if start:
                load_theme(True)
                pygame.mixer.music.queue(load_theme(True))
                pygame.mixer.music.play()
                break
            clock.tick(fps)
            screen.fill(black)
            screen.blit(text, textpos)
            pygame.display.flip()


intro()

result = None
speedup = False
currentspeed = ball.speed
volume = pygame.mixer.music.get_volume()
while True:
    game_over = False
    while not start:
        for i in range(0, 255, 2):
            text1 = smallfont.render("Press any key to start the game", True, (i, i, i))
            text1pos = text1.get_rect(centerx=background.get_width() / 2)
            text1pos.top = 400
            text2 = font.render("You win!", True, green)
            text2pos = text2.get_rect(centerx=background.get_width() / 2)
            text2pos.top = 300
            text3 = font.render("Game over", True, red)
            text3pos = text3.get_rect(centerx=background.get_width() / 2)
            text3pos.top = 300
            for event in pygame.event.get():
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
                    else:
                        start = True
                        break
            if start:
                load_theme(True)
                pygame.mixer.music.queue(load_theme(True))
                pygame.mixer.music.play()
                break
            clock.tick(fps)
            screen.fill(black)
            allsprites.remove(ball)
            allsprites.draw(screen)
            allsprites.add(ball)
            screen.blit(text1, text1pos)
            if result == "Victory":
                screen.blit(text2, text2pos)
            elif result == "Defeat":
                screen.blit(text3, text3pos)
            pygame.display.flip()
        for i in range(255, 0, -2):
            text1 = smallfont.render("Press any key to start the game", True, (i, i, i))
            text1pos = text1.get_rect(centerx=background.get_width() / 2)
            text1pos.top = 400
            text2 = font.render("You win!", True, green)
            text2pos = text2.get_rect(centerx=background.get_width() / 2)
            text2pos.top = 300
            text3 = font.render("Game over", True, red)
            text3pos = text3.get_rect(centerx=background.get_width() / 2)
            text3pos.top = 300
            for event in pygame.event.get():
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
                    else:
                        start = True
                        break
            if start:
                load_theme(True)
                pygame.mixer.music.queue(load_theme(True))
                pygame.mixer.music.play()
                break
            clock.tick(fps)
            screen.fill(black)
            allsprites.remove(ball)
            allsprites.draw(screen)
            allsprites.add(ball)
            screen.blit(text1, text1pos)
            if result == "Victory":
                screen.blit(text2, text2pos)
            elif result == "Defeat":
                screen.blit(text3, text3pos)
            pygame.display.flip()

    top = 50
    ncolumn = 32
    nrow = 4
    for row in range(nrow):
        for column in range(0, ncolumn):
            block = Block(random.choice(colors), column * (block_width + 2) + 1, top)
            blocks.add(block)
            allsprites.add(block)
        top += block_height + 2
    ball.x = random.randint(0, 780)
    ball.y = 180.0
    ball.direction = random.choice(ball.directions)
    ball.speed = 1.2

    while not game_over:
        clock.tick(fps)
        screen.fill(black)
        if pygame.mixer.music.get_endevent():
            pygame.mixer.music.queue(load_theme(True))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LALT or event.key == K_RALT:
                    if event.mod == KMOD_ALT:
                        if event.key == K_F4:
                            pygame.quit()
                            sys.exit()
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

        pausecheck()

        if not ball.update():
            player.update()
        if ball.update() and len(blocks) > 0:
            result = "Defeat"
            whoosh.play()
            pygame.mixer.music.stop()
            game_over = True

        if pygame.sprite.spritecollide(player, balls, False):
            ball.y -= 5
            difference = player.rect.centerx - ball.rect.centerx
            ball.bounce(difference)
            ball.speed += 0.04

        deadblocks = pygame.sprite.spritecollide(ball, blocks, True)
        if len(deadblocks) > 0:
            ball.bounce(0)
            if len(blocks) == 0:
                result = "Victory"
                whoosh.play()
                pygame.mixer.music.stop()
                game_over = True
        allsprites.draw(screen)
        pygame.display.flip()
        start = False
