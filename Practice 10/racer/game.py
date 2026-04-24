import os
import pygame
import random

pygame.init()
pygame.mixer.init()

# Размер окна
WIDTH = 500
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 0)
RED = (200, 0, 0)

font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 60)

# Путь к папке game.py
BASE_DIR = os.path.dirname(__file__)

# Путь к папке resources
RESOURCES = os.path.join(BASE_DIR, "resources")

# Загружаем картинки
background = pygame.image.load(os.path.join(RESOURCES, "AnimatedStreet.png"))
player = pygame.image.load(os.path.join(RESOURCES, "Player.png"))
enemy = pygame.image.load(os.path.join(RESOURCES, "Enemy.png"))

# Подгоняем размер картинок
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
player = pygame.transform.scale(player, (50, 90))
enemy = pygame.transform.scale(enemy, (50, 90))

# Загружаем звуки
pygame.mixer.music.load(os.path.join(RESOURCES, "background.wav"))
crash_sound = pygame.mixer.Sound(os.path.join(RESOURCES, "crash.wav"))


def show_game_over(coins):
    """
    Показывает экран Game Over.
    Если игрок нажмёт A, игра начнётся заново.
    Если игрок нажмёт Q, игра закроется.
    """
    screen.fill(RED)

    game_over_text = big_font.render("GAME OVER", True, WHITE)
    coins_text = font.render("Coins collected: " + str(coins), True, WHITE)
    restart_text = font.render("Press A to play again", True, WHITE)
    quit_text = font.render("Press Q to quit", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 190))
    screen.blit(coins_text, (WIDTH // 2 - coins_text.get_width() // 2, 270))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 330))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 370))

    pygame.display.update()

    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    return True

                if event.key == pygame.K_q:
                    return False


def play_game():
    """Основная функция игры."""

    # Запускаем музыку сначала при каждом новом запуске игры
    pygame.mixer.music.play(-1)

    # Игрок
    player_x = WIDTH // 2 - 25
    player_y = 500
    player_speed = 6

    # Враг
    enemy_x = random.randint(110, 340)
    enemy_y = -100
    enemy_speed = 5

    # Монетка
    coin_x = random.randint(120, 360)
    coin_y = -250
    coin_radius = 13
    coin_speed = 4

    # Счётчик монет
    coins = 0

    # Для движения фона
    background_y1 = 0
    background_y2 = -HEIGHT
    background_speed = 5

    running = True

    while running:
        clock.tick(60)

        # Закрытие окна
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # Управление машиной
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_x -= player_speed

        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # Ограничиваем машину, чтобы она оставалась на дороге
        if player_x < 90:
            player_x = 90

        if player_x > 360:
            player_x = 360

        # Двигаем фон вниз
        background_y1 += background_speed
        background_y2 += background_speed

        if background_y1 >= HEIGHT:
            background_y1 = -HEIGHT

        if background_y2 >= HEIGHT:
            background_y2 = -HEIGHT

        # Двигаем врага вниз
        enemy_y += enemy_speed

        if enemy_y > HEIGHT:
            enemy_y = -100
            enemy_x = random.randint(110, 340)

        # Двигаем монетку вниз
        coin_y += coin_speed

        if coin_y > HEIGHT:
            coin_y = -250
            coin_x = random.randint(120, 360)

        # Прямоугольники для столкновений
        player_rect = pygame.Rect(player_x, player_y, 50, 90)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, 50, 90)

        coin_rect = pygame.Rect(
            coin_x - coin_radius,
            coin_y - coin_radius,
            coin_radius * 2,
            coin_radius * 2
        )

        # Если случилась авария
        if player_rect.colliderect(enemy_rect):
            crash_sound.play()
            pygame.mixer.music.stop()

            # True = повторить игру, False = выйти
            return show_game_over(coins)

        # Если собрали монету
        if player_rect.colliderect(coin_rect):
            coins += 1
            coin_y = -250
            coin_x = random.randint(120, 360)

        # Рисуем фон
        screen.blit(background, (0, background_y1))
        screen.blit(background, (0, background_y2))

        # Рисуем врага и игрока
        screen.blit(enemy, (enemy_x, enemy_y))
        screen.blit(player, (player_x, player_y))

        # Рисуем монетку
        pygame.draw.circle(screen, YELLOW, (coin_x, coin_y), coin_radius)
        pygame.draw.circle(screen, WHITE, (coin_x, coin_y), 7, 2)

        # Счётчик монет справа сверху
        text = font.render("Coins: " + str(coins), True, BLACK)
        screen.blit(text, (WIDTH - text.get_width() - 15, 10))

        pygame.display.update()


# Главный цикл всей программы
play_again = True

while play_again:
    play_again = play_game()

pygame.quit()