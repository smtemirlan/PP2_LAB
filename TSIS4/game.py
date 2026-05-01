import random

import pygame

from db import get_best_score


WIDTH = 600
HEIGHT = 600

CELL = 20
TOP = 60

COLS = WIDTH // CELL
ROWS = (HEIGHT - TOP) // CELL

FPS = 60

FOOD_TIME = 8000
POWER_TIME = 8000
EFFECT_TIME = 5000


def draw_text(screen, text, size, x, y, color=(255, 255, 255), center=True):
    # Рисует текст
    font = pygame.font.SysFont("arial", size)
    img = font.render(text, True, color)
    rect = img.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(img, rect)


def cell_rect(pos):
    # Переводит клетку в прямоугольник Pygame
    x, y = pos
    return pygame.Rect(x * CELL, TOP + y * CELL, CELL, CELL)


def random_cell(snake, food, power, walls):
    # Ищет свободную клетку
    busy = set(snake)
    busy.update(walls)

    if food:
        busy.add(food["pos"])

    if power:
        busy.add(power["pos"])

    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))

        if pos not in busy:
            return pos


def make_food(snake, power, walls):
    # Создает еду
    kind = random.choice(["normal", "normal", "normal", "big", "poison"])
    pos = random_cell(snake, None, power, walls)

    if kind == "big":
        color = (255, 200, 0)
        points = 3
    elif kind == "poison":
        color = (150, 0, 0)
        points = -1
    else:
        color = (230, 40, 40)
        points = 1

    return {
        "kind": kind,
        "pos": pos,
        "color": color,
        "points": points,
        "born": pygame.time.get_ticks()
    }


def make_power(snake, food, walls):
    # Создает усиление
    kind = random.choice(["speed", "slow", "shield"])
    pos = random_cell(snake, food, None, walls)

    colors = {
        "speed": (0, 200, 255),
        "slow": (170, 80, 255),
        "shield": (40, 120, 255)
    }

    return {
        "kind": kind,
        "pos": pos,
        "color": colors[kind],
        "born": pygame.time.get_ticks()
    }


def make_walls(level, snake, food, power):
    # Создает препятствия с 3 уровня
    if level < 3:
        return []

    walls = []
    count = min(6 + level, 18)
    head = snake[0]

    while len(walls) < count:
        pos = (random.randint(1, COLS - 2), random.randint(1, ROWS - 2))

        # Не ставим стену рядом с головой
        near_head = abs(pos[0] - head[0]) + abs(pos[1] - head[1]) < 5

        if near_head:
            continue

        if pos in snake or pos in walls:
            continue

        if food and pos == food["pos"]:
            continue

        if power and pos == power["pos"]:
            continue

        walls.append(pos)

    return walls


def get_delay(level, active_power, effect_until):
    # Считает скорость змеи
    now = pygame.time.get_ticks()
    delay = max(70, 170 - (level - 1) * 12)

    if now < effect_until and active_power == "speed":
        delay = max(45, delay - 45)

    if now < effect_until and active_power == "slow":
        delay += 70

    return delay


def draw_game(screen, snake, food, power, walls, settings, score, level, best, active_power, effect_until, shield):
    # Рисует поле
    screen.fill((20, 20, 25))

    pygame.draw.rect(screen, (35, 35, 45), (0, 0, WIDTH, TOP))

    draw_text(screen, f"Score: {score}", 20, 10, 10, center=False)
    draw_text(screen, f"Level: {level}", 20, 130, 10, center=False)
    draw_text(screen, f"Best: {best}", 20, 240, 10, center=False)

    power_text = "Power: none"

    now = pygame.time.get_ticks()
    if active_power in ["speed", "slow"] and now < effect_until:
        left = (effect_until - now) // 1000 + 1
        power_text = f"Power: {active_power} {left}s"

    if shield:
        power_text = "Power: shield"

    draw_text(screen, power_text, 20, 360, 10, center=False)

    if settings.get("grid", True):
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(screen, (35, 35, 40), (x, TOP), (x, HEIGHT))

        for y in range(TOP, HEIGHT, CELL):
            pygame.draw.line(screen, (35, 35, 40), (0, y), (WIDTH, y))

    for wall in walls:
        pygame.draw.rect(screen, (110, 110, 110), cell_rect(wall))

    if food:
        pygame.draw.rect(screen, food["color"], cell_rect(food["pos"]))

    if power:
        pygame.draw.rect(screen, power["color"], cell_rect(power["pos"]))
        draw_text(screen, power["kind"][0].upper(), 17, cell_rect(power["pos"]).centerx, cell_rect(power["pos"]).centery)

    snake_color = tuple(settings.get("snake_color", [0, 180, 80]))

    for i, part in enumerate(snake):
        color = (0, 255, 120) if i == 0 else snake_color
        pygame.draw.rect(screen, color, cell_rect(part).inflate(-2, -2), border_radius=4)

    if shield:
        pygame.draw.rect(screen, (40, 120, 255), cell_rect(snake[0]).inflate(6, 6), 3, border_radius=6)

    pygame.display.flip()


def play_game(screen, player_name, settings):
    # Главный игровой цикл
    clock = pygame.time.Clock()
    best = get_best_score(player_name)

    snake = [(COLS // 2, ROWS // 2), (COLS // 2 - 1, ROWS // 2), (COLS // 2 - 2, ROWS // 2)]
    direction = (1, 0)
    next_direction = (1, 0)

    score = 0
    level = 1
    grow = 0

    active_power = "none"
    effect_until = 0
    shield = False

    walls = []
    power = None
    food = make_food(snake, power, walls)

    last_move = pygame.time.get_ticks()
    last_power_spawn = pygame.time.get_ticks()

    while True:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None

                if event.key == pygame.K_UP and direction != (0, 1):
                    next_direction = (0, -1)

                if event.key == pygame.K_DOWN and direction != (0, -1):
                    next_direction = (0, 1)

                if event.key == pygame.K_LEFT and direction != (1, 0):
                    next_direction = (-1, 0)

                if event.key == pygame.K_RIGHT and direction != (-1, 0):
                    next_direction = (1, 0)

        # Еда исчезает по таймеру
        if food and now - food["born"] > FOOD_TIME:
            food = make_food(snake, power, walls)

        # Усиление появляется иногда
        if power is None and now - last_power_spawn > 5000:
            if random.randint(1, 100) <= 35:
                power = make_power(snake, food, walls)
            last_power_spawn = now

        # Усиление исчезает по таймеру
        if power and now - power["born"] > POWER_TIME:
            power = None

        delay = get_delay(level, active_power, effect_until)

        if now - last_move >= delay:
            direction = next_direction
            last_move = now

            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])

            hit_wall = (
                new_head[0] < 0 or new_head[0] >= COLS or
                new_head[1] < 0 or new_head[1] >= ROWS
            )

            if hit_wall and shield:
                shield = False
                new_head = (new_head[0] % COLS, new_head[1] % ROWS)

            elif hit_wall:
                return {
                    "score": score,
                    "level": level
                }

            hit_self = new_head in snake
            hit_block = new_head in walls

            if (hit_self or hit_block) and shield:
                shield = False

                if hit_block:
                    walls.remove(new_head)

            elif hit_self or hit_block:
                return {
                    "score": score,
                    "level": level
                }

            snake.insert(0, new_head)

            ate_food = food and new_head == food["pos"]
            ate_power = power and new_head == power["pos"]

            if ate_food:
                if food["kind"] == "poison":
                    if len(snake) <= 4:
                        return {
                            "score": score,
                            "level": level
                        }

                    # Яд режет змею на 2 клетки
                    snake.pop()
                    snake.pop()
                    score = max(0, score - 1)

                elif food["kind"] == "big":
                    score += food["points"]
                    grow += 2

                else:
                    score += food["points"]
                    grow += 1

                old_level = level
                level = score // 5 + 1

                if level != old_level:
                    walls = make_walls(level, snake, food, power)

                food = make_food(snake, power, walls)

            if ate_power:
                if power["kind"] == "shield":
                    shield = True
                    active_power = "shield"
                else:
                    active_power = power["kind"]
                    effect_until = now + EFFECT_TIME

                power = None

            if grow > 0:
                grow -= 1
            else:
                snake.pop()

        draw_game(screen, snake, food, power, walls, settings, score, level, best, active_power, effect_until, shield)
        clock.tick(FPS)
