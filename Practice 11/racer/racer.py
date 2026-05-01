import pygame
import sys
import random
from pathlib import Path
from pygame.locals import *


BASE_DIR = Path(__file__).resolve().parent

pygame.init()
pygame.mixer.init()

FPS = 60
FramePerSec = pygame.time.Clock()

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

START_SPEED = 5

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

game_over_text = font.render("Game Over", True, BLACK)
play_again_text = font_small.render("Press A to play again", True, BLACK)
quit_text = font_small.render("Press Q to quit", True, BLACK)

background = pygame.image.load(str(BASE_DIR / "images" / "AnimatedStreet.png"))


def start_background_music():
    music_files = [
        "background.mp3",
        "background.wav",
        "music.mp3",
        "music.wav",
        "background_music.mp3",
        "background_music.wav",
    ]

    for file_name in music_files:
        music_path = BASE_DIR / "sounds" / file_name

        if music_path.exists():
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
            return

    print("Фоновая музыка не найдена в папке sounds.")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(str(BASE_DIR / "images" / "Enemy.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self, speed):
        self.rect.move_ip(0, speed)

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            return 1

        return 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(str(BASE_DIR / "images" / "Player.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)


class Coin1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(str(BASE_DIR / "images" / "Power1.png"))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self, speed):
        self.rect.move_ip(0, speed)

        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Coin2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(str(BASE_DIR / "images" / "Power2.png"))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self, speed):
        self.rect.move_ip(0, speed)

        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


def game_over_screen():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return False

            if event.type == KEYDOWN:
                if event.key == K_a:
                    return True

                if event.key == K_q:
                    return False

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over_text, (30, 220))
        DISPLAYSURF.blit(play_again_text, (90, 310))
        DISPLAYSURF.blit(quit_text, (130, 340))

        pygame.display.update()
        FramePerSec.tick(FPS)


def run_game():
    speed = START_SPEED
    score = 0
    coins = 0
    coins_speed = 0

    P1 = Player()
    E1 = Enemy()
    C1 = Coin1()
    C2 = Coin2()

    enemies = pygame.sprite.Group()
    coin1 = pygame.sprite.Group()
    coin2 = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    enemies.add(E1)
    coin1.add(C1)
    coin2.add(C2)

    all_sprites.add(P1)
    all_sprites.add(E1)
    all_sprites.add(C1)
    all_sprites.add(C2)

    crash_sound = pygame.mixer.Sound(str(BASE_DIR / "sounds" / "crash.wav"))

    start_background_music()

    INC_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INC_SPEED, 1000)

    while True:
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                speed += 0.125

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.blit(background, (0, 0))

        scores = font_small.render(f"Score: {score}", True, BLACK)
        DISPLAYSURF.blit(scores, (10, 10))

        coin_text = font_small.render(f"Coins: {coins}", True, BLACK)
        DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 120, 10))

        P1.move()
        score += E1.move(speed)
        C1.move(speed)
        C2.move(speed)

        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)

        coin_hit1 = pygame.sprite.spritecollideany(P1, coin1)

        if coin_hit1:
            coins += 1
            coin_hit1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

        coin_hit2 = pygame.sprite.spritecollideany(P1, coin2)

        if coin_hit2:
            coins += 2
            coin_hit2.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

        if coins != 0 and coins // 10 > coins_speed:
            speed += 0.125
            coins_speed = coins // 10

        if pygame.sprite.spritecollideany(P1, enemies):
            pygame.mixer.music.stop()
            crash_sound.play()

            pygame.time.wait(1000)

            play_again = game_over_screen()

            if play_again:
                pygame.mixer.music.stop()
                return

            pygame.quit()
            sys.exit()

        pygame.display.update()
        FramePerSec.tick(FPS)


while True:
    run_game()