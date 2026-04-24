import pygame
import math

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 220)
YELLOW = (255, 220, 0)
GRAY = (200, 200, 200)

font = pygame.font.SysFont("Arial", 22)

# Заливаем фон белым
screen.fill(WHITE)

# Настройки
color = BLACK
tool = "brush"
brush_size = 6
eraser_size = 25

drawing = False
start_pos = None
last_pos = None


def draw_menu():
    """Рисует верхнее меню."""
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 70))

    text = font.render("1 Brush | 2 Rectangle | 3 Circle | E Eraser | C Clear", True, BLACK)
    screen.blit(text, (10, 8))

    # Цвета
    pygame.draw.rect(screen, BLACK, (10, 40, 25, 20))
    pygame.draw.rect(screen, RED, (45, 40, 25, 20))
    pygame.draw.rect(screen, GREEN, (80, 40, 25, 20))
    pygame.draw.rect(screen, BLUE, (115, 40, 25, 20))
    pygame.draw.rect(screen, YELLOW, (150, 40, 25, 20))

    # Показываем текущий инструмент
    tool_text = font.render("Tool: " + tool, True, BLACK)
    screen.blit(tool_text, (220, 38))


def get_color(pos):
    """Выбор цвета мышкой."""
    x, y = pos

    if 40 <= y <= 60:
        if 10 <= x <= 35:
            return BLACK
        if 45 <= x <= 70:
            return RED
        if 80 <= x <= 105:
            return GREEN
        if 115 <= x <= 140:
            return BLUE
        if 150 <= x <= 175:
            return YELLOW

    return None


running = True

while running:
    clock.tick(60)

    draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Выбор инструмента
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                tool = "brush"

            if event.key == pygame.K_2:
                tool = "rectangle"

            if event.key == pygame.K_3:
                tool = "circle"

            if event.key == pygame.K_e:
                tool = "eraser"

            if event.key == pygame.K_c:
                screen.fill(WHITE)

        # Нажали мышь
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Если кликнули на цвет
            selected_color = get_color(mouse_pos)

            if selected_color is not None:
                color = selected_color
                tool = "brush"

            # Если кликнули ниже меню, можно рисовать
            elif mouse_pos[1] > 70:
                drawing = True
                start_pos = mouse_pos
                last_pos = mouse_pos

        # Двигаем мышь с зажатой кнопкой
        if event.type == pygame.MOUSEMOTION and drawing:
            mouse_pos = pygame.mouse.get_pos()

            if mouse_pos[1] > 70:
                if tool == "brush":
                    pygame.draw.line(screen, color, last_pos, mouse_pos, brush_size)
                    pygame.draw.circle(screen, color, mouse_pos, brush_size // 2)
                    last_pos = mouse_pos

                if tool == "eraser":
                    pygame.draw.line(screen, WHITE, last_pos, mouse_pos, eraser_size)
                    pygame.draw.circle(screen, WHITE, mouse_pos, eraser_size // 2)
                    last_pos = mouse_pos

        # Отпустили мышь
        if event.type == pygame.MOUSEBUTTONUP and drawing:
            mouse_pos = pygame.mouse.get_pos()

            if tool == "rectangle":
                x1, y1 = start_pos
                x2, y2 = mouse_pos

                rect_x = min(x1, x2)
                rect_y = min(y1, y2)
                rect_w = abs(x2 - x1)
                rect_h = abs(y2 - y1)

                pygame.draw.rect(screen, color, (rect_x, rect_y, rect_w, rect_h), 3)

            if tool == "circle":
                x1, y1 = start_pos
                x2, y2 = mouse_pos

                radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
                pygame.draw.circle(screen, color, start_pos, radius, 3)

            drawing = False

    pygame.display.update()

pygame.quit()