import pygame
import math
from datetime import datetime

# ---------- БАЗОВЫЕ НАСТРОЙКИ ----------
pygame.init()

WIDTH, HEIGHT = 1000, 700
TOOLBAR_H = 110

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 11 - Paint")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)
DARK = (40, 40, 40)
RED = (230, 40, 40)
GREEN = (0, 200, 60)
BLUE = (40, 90, 240)
YELLOW = (250, 230, 0)
PURPLE = (160, 60, 220)

colors = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE]
current_color = BLACK

# Инструменты
tools = [
    "pencil",
    "rect",
    "square",
    "right triangle",
    "equal triangle",
    "rhombus"
]

current_tool = "pencil"
brush_size = 3

drawing = False
start_pos = None
last_pos = None

# Отдельный холст, на нем хранится рисунок
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_H))
canvas.fill(WHITE)

# Кнопки инструментов
tool_buttons = []
x = 10

for name in tools:
    rect = pygame.Rect(x, 10, 150, 35)
    tool_buttons.append((rect, name))
    x += 160

# Кнопки цветов
color_buttons = []
x = 10

for color in colors:
    rect = pygame.Rect(x, 60, 40, 35)
    color_buttons.append((rect, color))
    x += 50

# Кнопки размеров кисти
size_buttons = []
x = 340

for size in [2, 5, 10]:
    rect = pygame.Rect(x, 60, 45, 35)
    size_buttons.append((rect, size))
    x += 55


def canvas_pos(pos):
    """Переводит координаты окна в координаты холста."""
    return pos[0], pos[1] - TOOLBAR_H


def in_canvas(pos):
    """Проверяет, находится ли мышь на холсте."""
    return pos[1] >= TOOLBAR_H


def draw_text(text, x, y, color=BLACK):
    """Выводит текст на экран."""
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_button(rect, text, active=False):
    """Рисует кнопку."""
    if active:
        color = (170, 210, 245)
    else:
        color = GRAY

    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, DARK, rect, 2)
    draw_text(text, rect.x + 8, rect.y + 7)


def draw_square(surface, color, start, end, width):
    """Рисует квадрат."""
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

    pygame.draw.rect(surface, color, rect, width)


def draw_right_triangle(surface, color, start, end, width):
    """Рисует прямоугольный треугольник."""
    x1, y1 = start
    x2, y2 = end

    points = [
        (x1, y1),
        (x1, y2),
        (x2, y2)
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_equal_triangle(surface, color, start, end, width):
    """Рисует равносторонний треугольник."""
    x1, y1 = start
    x2, y2 = end

    side = abs(x2 - x1)

    if side < 5:
        return

    triangle_height = int(side * math.sqrt(3) / 2)

    if y2 < y1:
        points = [
            (x1, y1),
            (x1 + side, y1),
            (x1 + side // 2, y1 - triangle_height)
        ]
    else:
        points = [
            (x1, y1),
            (x1 + side, y1),
            (x1 + side // 2, y1 + triangle_height)
        ]

    pygame.draw.polygon(surface, color, points, width)


def draw_rhombus(surface, color, start, end, width):
    """Рисует ромб."""
    x1, y1 = start
    x2, y2 = end

    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    points = [
        (center_x, y1),
        (x2, center_y),
        (center_x, y2),
        (x1, center_y)
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_shape(surface, tool, color, start, end, width):
    """Выбирает фигуру и рисует ее."""
    x1, y1 = start
    x2, y2 = end

    if tool == "rect":
        rect = pygame.Rect(
            min(x1, x2),
            min(y1, y2),
            abs(x2 - x1),
            abs(y2 - y1)
        )
        pygame.draw.rect(surface, color, rect, width)

    elif tool == "square":
        draw_square(surface, color, start, end, width)

    elif tool == "right triangle":
        draw_right_triangle(surface, color, start, end, width)

    elif tool == "equal triangle":
        draw_equal_triangle(surface, color, start, end, width)

    elif tool == "rhombus":
        draw_rhombus(surface, color, start, end, width)


def save_canvas():
    """Сохраняет холст в PNG."""
    filename = "paint_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
    pygame.image.save(canvas, filename)
    print("Saved:", filename)


running = True

while running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()

    # ---------- СОБЫТИЯ ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Ctrl + S сохраняет картинку
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas()

        # Нажатие мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # Если нажали на верхнюю панель
            if not in_canvas(event.pos):

                # Выбор инструмента
                for rect, name in tool_buttons:
                    if rect.collidepoint(event.pos):
                        current_tool = name

                # Выбор цвета
                for rect, color in color_buttons:
                    if rect.collidepoint(event.pos):
                        current_color = color

                # Выбор размера кисти
                for rect, size in size_buttons:
                    if rect.collidepoint(event.pos):
                        brush_size = size

            # Если нажали на холст
            else:
                drawing = True
                start_pos = canvas_pos(event.pos)
                last_pos = start_pos

        # Отпустили мышь
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drawing:
                end_pos = canvas_pos(event.pos)

                # Фигуры рисуются после отпускания мыши
                if current_tool != "pencil":
                    draw_shape(
                        canvas,
                        current_tool,
                        current_color,
                        start_pos,
                        end_pos,
                        brush_size
                    )

                drawing = False
                start_pos = None
                last_pos = None

        # Движение мыши
        if event.type == pygame.MOUSEMOTION:

            # Карандаш рисует сразу
            if drawing and current_tool == "pencil" and in_canvas(event.pos):
                pos = canvas_pos(event.pos)

                pygame.draw.line(
                    canvas,
                    current_color,
                    last_pos,
                    pos,
                    brush_size
                )

                last_pos = pos

    # ---------- ОТРИСОВКА ----------
    screen.fill(GRAY)

    # Инструменты
    for rect, name in tool_buttons:
        draw_button(rect, name, current_tool == name)

    # Цвета
    for rect, color in color_buttons:
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, DARK, rect, 2)

        if color == current_color:
            pygame.draw.rect(screen, WHITE, rect, 4)

    # Размер кисти
    draw_text("Size:", 285, 67)

    for rect, size in size_buttons:
        draw_button(rect, str(size), brush_size == size)

    draw_text("Ctrl+S save", 520, 67)

    # Сам холст
    screen.blit(canvas, (0, TOOLBAR_H))

    # Предпросмотр фигуры
    if drawing and current_tool != "pencil" and in_canvas(mouse_pos):
        preview = canvas.copy()

        draw_shape(
            preview,
            current_tool,
            current_color,
            start_pos,
            canvas_pos(mouse_pos),
            brush_size
        )

        screen.blit(preview, (0, TOOLBAR_H))

    pygame.display.update()

pygame.quit()
