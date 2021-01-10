import pygame
import random
from math import *

clock = pygame.time.Clock()
WIDTH = 800
HEIGHT = 600
FPS = 100


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Убей как можно больше жуков",
                  "Не дай жукам скрыться из виду"]

    fon = pygame.transform.scale(pygame.image.load('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


class Insect(pygame.sprite.Sprite):
    def __init__(self, rect_x=0, rect_y=0):
        self.shablon = self.image = pygame.image.load(random.choice(bugs))
        self.rect_x = rect_x
        self.rect_y = rect_y
        self.steps = 0

        self.vx = random.randint(0, 2)
        if self.vx == 0:
            self.vx = -1
        self.vy = random.randint(0, 2)
        if self.vy == 0:
            self.vy = 1

    # Функция поворачивает изображение в соответствии с движением жука
    def rotate(self, degree):
        self.shablon = pygame.transform.rotate(self.image, degree)

    def step(self, x, y):
        self.rect_x += x
        self.rect_y += y
        self.steps += 1

    def destroy(self):
        global dead_bugs, score
        if score > 40000:
            return
        dead_bugs += 1
        score += 100 / self.steps * 2
        pygame.time.delay(2000)
        if score > 40000:
            self.shablon = self.image = pygame.image.load("dead.png")
            new_bug()
            return
        if dead_bugs % 20 == 0:
            self.shablon = self.image = pygame.image.load('gold_insect.jpg')
            score += 100 / self.steps * 2
        else:
            self.shablon = self.image = pygame.image.load(random.choice(bugs))
        self.steps = 0
        new_bug()


def end():
    exit()


# Функция изменяет направление движения жука, если они бьются об стену
def update():
    global WIDTH, HEIGHT
    if INSECT.rect_x < 0 or INSECT.rect_x > WIDTH - 70:
        INSECT.vx = -INSECT.vx
    if INSECT.rect_y > HEIGHT:
        end()


# Функция меняет координаты текущего жука на начальные(но рандомные)
def new_bug():
    INSECT.rect_x, INSECT.rect_y = random.randint(0, HEIGHT - 60), 0
    INSECT.vx = random.randint(0, 2)
    if INSECT.vx == 0:
        INSECT.vx = -1
    INSECT.vy = random.randint(0, 2)
    if INSECT.vy == 0:
        INSECT.vy = 1


all_sprites = pygame.sprite.Group()

bugs = ["insect.jpg", "insect1.jpg", "insect2.jpg", "insect3.jpg", "insect4.jpg", "insect5.jpg", "insect6.jpg",
        "insect7.jpg", "insect8.jpg", "insect9.jpg"]
Color = (255, 255, 255)
degree = 0
score = 0
dead_bugs = 0
BackGround = Background('screen.jpg', [0, 0])

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init()
start_screen()
pygame.key.set_repeat(20, 20)
pygame.display.set_caption("BugHunter")
INSECT = Insect(random.randint(0, HEIGHT - 60), 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            event_x, event_y = pygame.mouse.get_pos()
            if event_x > INSECT.rect_x and event_x < INSECT.rect_x + 60 \
                    and event_y > INSECT.rect_y and event_y < INSECT.rect_y + 60:
                INSECT.destroy()

    update()

    # Расчет для функции rotate
    degree = atan2(-INSECT.vy, INSECT.vx)
    degree = degrees(degree) - 90
    INSECT.rotate(degree)

    INSECT.step(INSECT.vx, INSECT.vy)
    pygame.time.delay(5)

    screen.fill(Color)
    screen.blit(BackGround.image, BackGround.rect)
    screen.blit(INSECT.shablon, (INSECT.rect_x, INSECT.rect_y))
    pygame.display.update()

pygame.quit()
