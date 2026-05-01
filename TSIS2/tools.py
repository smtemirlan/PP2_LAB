import pygame
from collections import deque


# Размер окна
WIDTH = 1000
HEIGHT = 700

# Верхняя панель
CANVAS_Y = 100

# Область холста
CANVAS_RECT = pygame.Rect(0, CANVAS_Y, WIDTH, HEIGHT - CANVAS_Y)


def in_canvas(pos):
    # Проверяет область холста
    return CANVAS_RECT.collidepoint(pos)


def canvas_pos(pos):
    # Координаты для холста
    x, y = pos
    return x, y - CANVAS_Y


def draw_line(surface, color, start, end, size):
    # Рисует прямую линию
    pygame.draw.line(surface, color, start, end, size)


def draw_rectangle(surface, color, start, end, size):
    # Рисует прямоугольник
    x1, y1 = start
    x2, y2 = end

    rect = pygame.Rect(
        min(x1, x2),
        min(y1, y2),
        abs(x2 - x1),
        abs(y2 - y1)
    )

    pygame.draw.rect(surface, color, rect, size)


def draw_circle(surface, color, start, end, size):
    # Рисует обычный круг
    x1, y1 = start
    x2, y2 = end

    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)

    if radius > 0:
        pygame.draw.circle(surface, color, start, radius, size)


def draw_square(surface, color, start, end, size):
    # Рисует ровный квадрат
    x1, y1 = start
    x2, y2 = end

    side = min(abs(x2 - x1), abs(y2 - y1))

    if x2 < x1:
        x2 = x1 - side
    else:
        x2 = x1 + side

    if y2 < y1:
        y2 = y1 - side
    else:
        y2 = y1 + side

    rect = pygame.Rect(
        min(x1, x2),
        min(y1, y2),
        side,
        side
    )

    pygame.draw.rect(surface, color, rect, size)


def draw_triangle(surface, color, start, end, size):
    # Рисует треугольник
    x1, y1 = start
    x2, y2 = end

    side = abs(x2 - x1)
    height = int(side * 0.866)

    if side < 5:
        return

    points = [
        (x1, y1),
        (x1 - side // 2, y1 + height),
        (x1 + side // 2, y1 + height)
    ]

    pygame.draw.polygon(surface, color, points, size)


def draw_rhombus(surface, color, start, end, size):
    # Рисует простой ромб
    x1, y1 = start
    x2, y2 = end

    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2

    points = [
        (cx, y1),
        (x2, cy),
        (cx, y2),
        (x1, cy)
    ]

    pygame.draw.polygon(surface, color, points, size)


def flood_fill(surface, start_pos, new_color):
    # Заливает одну область
    width, height = surface.get_size()
    x, y = start_pos

    if not (0 <= x < width and 0 <= y < height):
        return

    old_color = surface.get_at((x, y))
    new_color = pygame.Color(new_color)

    if old_color == new_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        x, y = queue.popleft()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        if surface.get_at((x, y)) != old_color:
            continue

        surface.set_at((x, y), new_color)

        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))


def draw_shape(surface, tool, color, start, end, size):
    # Выбирает нужную фигуру
    if tool == "line":
        draw_line(surface, color, start, end, size)

    elif tool == "rect":
        draw_rectangle(surface, color, start, end, size)

    elif tool == "circle":
        draw_circle(surface, color, start, end, size)

    elif tool == "square":
        draw_square(surface, color, start, end, size)

    elif tool == "triangle":
        draw_triangle(surface, color, start, end, size)

    elif tool == "rhombus":
        draw_rhombus(surface, color, start, end, size)