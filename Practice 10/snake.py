import pygame
import random

pygame.init()

# Размеры
WIDTH = 600
HEIGHT = 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (220, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

font = pygame.font.SysFont("Arial", 28)

# Змейка
snake = [(100, 100), (80, 100), (60, 100)]
dx = CELL
dy = 0

# Очки и уровень
score = 0
level = 1
speed = 8

def create_food():
    """Создаёт еду не на стене и не на змейке."""
    while True:
        x = random.randrange(CELL, WIDTH - CELL, CELL)
        y = random.randrange(CELL, HEIGHT - CELL, CELL)

        if (x, y) not in snake:
            return x, y

food = create_food()

running = True
while running:
    clock.tick(speed)

    # События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Управление
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy == 0:
                dx = 0
                dy = -CELL

            if event.key == pygame.K_DOWN and dy == 0:
                dx = 0
                dy = CELL

            if event.key == pygame.K_LEFT and dx == 0:
                dx = -CELL
                dy = 0

            if event.key == pygame.K_RIGHT and dx == 0:
                dx = CELL
                dy = 0

    # Новая голова змейки
    head_x = snake[0][0] + dx
    head_y = snake[0][1] + dy
    new_head = (head_x, head_y)

    # Проверка столкновения со стеной
    if head_x <= 0 or head_x >= WIDTH - CELL or head_y <= 0 or head_y >= HEIGHT - CELL:
        running = False

    # Проверка столкновения с самой собой
    if new_head in snake:
        running = False

    # Добавляем новую голову
    snake.insert(0, new_head)

    # Если съели еду
    if new_head == food:
        score += 1

        # Новый уровень каждые 4 еды
        if score % 4 == 0:
            level += 1
            speed += 2

        food = create_food()
    else:
        # Если еду не съели, удаляем хвост
        snake.pop()

    # Рисование
    screen.fill(BLACK)

    # Стены
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, CELL))
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - CELL, WIDTH, CELL))
    pygame.draw.rect(screen, GRAY, (0, 0, CELL, HEIGHT))
    pygame.draw.rect(screen, GRAY, (WIDTH - CELL, 0, CELL, HEIGHT))

    # Еда
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL, CELL))

    # Змейка
    for part in snake:
        pygame.draw.rect(screen, GREEN, (part[0], part[1], CELL, CELL))

    # Счёт и уровень
    text = font.render("Score: " + str(score) + "  Level: " + str(level), True, WHITE)
    screen.blit(text, (30, 30))

    pygame.display.update()

pygame.quit()