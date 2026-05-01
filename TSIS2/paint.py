import pygame
from datetime import datetime
from pathlib import Path

# Импортируем настройки и функции рисования из tools.py
from tools import (
    WIDTH,
    HEIGHT,
    CANVAS_Y,
    in_canvas,
    canvas_pos,
    flood_fill,
    draw_shape
)


# Запускаем pygame
pygame.init()

# Создаём главное окно программы
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

# Clock нужен, чтобы ограничить FPS
clock = pygame.time.Clock()

# Шрифты для кнопок и текста
font = pygame.font.SysFont("arial", 18)
small_font = pygame.font.SysFont("arial", 15)

# Холст для рисования.
# Мы рисуем не сразу на screen, а на отдельной поверхности canvas.
canvas = pygame.Surface((WIDTH, HEIGHT - CANVAS_Y))
canvas.fill("white")

# Папка, куда сохраняются картинки
SAVE_DIR = Path(__file__).parent / "saved"
SAVE_DIR.mkdir(exist_ok=True)

# Текущий выбранный инструмент
current_tool = "pencil"

# Текущий цвет
current_color = pygame.Color("black")

# Текущий размер кисти
brush_size = 5

# Переменные для рисования мышкой
drawing = False
start_pos = None
last_pos = None

# Переменные для текстового инструмента
text_mode = False
text_pos = None
text_value = ""


# Список инструментов.
# Первый элемент — внутреннее имя, второй — текст на кнопке.
TOOLS = [
    ("pencil", "Pencil"),
    ("line", "Line"),
    ("eraser", "Eraser"),
    ("rect", "Rect"),
    ("circle", "Circle"),
    ("square", "Square"),
    ("triangle", "Triangle"),
    ("rhombus", "Rhombus"),
    ("fill", "Fill"),
    ("text", "Text"),
]


# Список цветов
COLORS = [
    ("black", pygame.Color("black")),
    ("red", pygame.Color("red")),
    ("green", pygame.Color("green")),
    ("blue", pygame.Color("blue")),
    ("yellow", pygame.Color("yellow")),
    ("purple", pygame.Color("purple")),
    ("orange", pygame.Color("orange")),
    ("white", pygame.Color("white")),
]


# Размеры кисти
SIZES = [
    (2, "1"),
    (5, "2"),
    (10, "3"),
]


# Здесь будут храниться кнопки
tool_buttons = []
color_buttons = []
size_buttons = []


def make_button(x, y, w, h, text, value):
    """
    Создаёт обычную кнопку.
    rect — область кнопки.
    text — текст на кнопке.
    value — значение, которое кнопка выбирает.
    """
    return {
        "rect": pygame.Rect(x, y, w, h),
        "text": text,
        "value": value
    }


def create_buttons():
    """
    Создаёт все кнопки:
    инструменты, цвета и размеры кисти.
    """
    global tool_buttons, color_buttons, size_buttons

    tool_buttons = []

    x = 10
    y = 10

    # Создаём кнопки инструментов в верхней строке
    for value, text in TOOLS:
        tool_buttons.append(make_button(x, y, 84, 28, text, value))
        x += 88

    color_buttons = []

    x = 10
    y = 65

    # Создаём цветные квадратики
    for name, color in COLORS:
        color_buttons.append({
            "rect": pygame.Rect(x, y, 28, 24),
            "color": color,
            "name": name
        })
        x += 34

    size_buttons = []

    x = 430
    y = 65

    # Создаём кнопки размера кисти: 1, 2, 3
    for size, text in SIZES:
        size_buttons.append(make_button(x, y, 40, 24, text, size))
        x += 45


# Вызываем функцию, чтобы кнопки появились
create_buttons()


def draw_button(button, active=False):
    """
    Рисует одну обычную кнопку.
    Если active=True, кнопка подсвечивается голубым.
    """
    rect = button["rect"]

    if active:
        pygame.draw.rect(screen, (170, 210, 245), rect)
    else:
        pygame.draw.rect(screen, (230, 230, 230), rect)

    pygame.draw.rect(screen, "black", rect, 1)

    label = small_font.render(button["text"], True, "black")
    screen.blit(label, (rect.x + 6, rect.y + 5))


def draw_toolbar():
    """
    Рисует всю верхнюю панель:
    кнопки инструментов, цвета, размер кисти и подсказку.
    """
    pygame.draw.rect(screen, (210, 210, 210), (0, 0, WIDTH, CANVAS_Y))
    pygame.draw.line(screen, "black", (0, CANVAS_Y), (WIDTH, CANVAS_Y), 2)

    # Рисуем кнопки инструментов
    for button in tool_buttons:
        draw_button(button, button["value"] == current_tool)

    # Рисуем цветные квадраты
    for button in color_buttons:
        rect = button["rect"]

        pygame.draw.rect(screen, button["color"], rect)
        pygame.draw.rect(screen, "black", rect, 2)

        # Если цвет выбран, рисуем рамку вокруг него
        if button["color"] == current_color:
            pygame.draw.rect(screen, "black", rect.inflate(6, 6), 2)

    # Надпись для размера кисти
    brush_text = font.render("Brush size:", True, "black")
    screen.blit(brush_text, (305, 66))

    # Кнопки размеров кисти
    for button in size_buttons:
        draw_button(button, button["value"] == brush_size)

    # Информация справа
    info = f"Tool: {current_tool} | Size: {brush_size} | Ctrl+S save | 1/2/3 size"
    info_text = small_font.render(info, True, "black")
    screen.blit(info_text, (590, 68))


def save_canvas():
    """
    Сохраняет холст в PNG-файл.
    В имени файла используется текущее время,
    чтобы старые сохранения не перезаписывались.
    """
    time_text = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = SAVE_DIR / f"canvas_{time_text}.png"

    pygame.image.save(canvas, filename)

    print("Saved:", filename)


def handle_toolbar_click(pos):
    """
    Проверяет, куда пользователь нажал на верхней панели.
    Может выбрать инструмент, цвет или размер кисти.
    """
    global current_tool, current_color, brush_size

    # Проверяем кнопки инструментов
    for button in tool_buttons:
        if button["rect"].collidepoint(pos):
            current_tool = button["value"]
            return True

    # Проверяем кнопки цветов
    for button in color_buttons:
        if button["rect"].collidepoint(pos):
            current_color = button["color"]
            return True

    # Проверяем кнопки размеров кисти
    for button in size_buttons:
        if button["rect"].collidepoint(pos):
            brush_size = button["value"]
            return True

    return False


def draw_text_preview():
    """
    Показывает текст во время ввода.
    Пока пользователь не нажал Enter,
    текст ещё не сохранён на canvas.
    """
    if text_mode and text_pos is not None:
        rendered = font.render(text_value + "|", True, current_color)
        screen.blit(rendered, (text_pos[0], text_pos[1] + CANVAS_Y))


def confirm_text():
    """
    Сохраняет введённый текст на холст.
    Вызывается при нажатии Enter.
    """
    global text_mode, text_pos, text_value

    if text_mode and text_pos is not None and text_value:
        rendered = font.render(text_value, True, current_color)
        canvas.blit(rendered, text_pos)

    text_mode = False
    text_pos = None
    text_value = ""


def cancel_text():
    """
    Отменяет ввод текста.
    Вызывается при нажатии Escape.
    """
    global text_mode, text_pos, text_value

    text_mode = False
    text_pos = None
    text_value = ""


# Главный цикл программы
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()

    # Переводим координаты мыши в координаты холста
    canvas_mouse_pos = canvas_pos(mouse_pos)

    # Обрабатываем все события pygame
    for event in pygame.event.get():

        # Закрытие окна
        if event.type == pygame.QUIT:
            running = False

        # Обработка клавиатуры
        elif event.type == pygame.KEYDOWN:

            # Если включён текстовый режим
            if text_mode:
                if event.key == pygame.K_RETURN:
                    confirm_text()

                elif event.key == pygame.K_ESCAPE:
                    cancel_text()

                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]

                else:
                    text_value += event.unicode

            # Если обычный режим
            else:
                if event.key == pygame.K_1:
                    brush_size = 2

                elif event.key == pygame.K_2:
                    brush_size = 5

                elif event.key == pygame.K_3:
                    brush_size = 10

                # Ctrl + S сохраняет холст
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save_canvas()

        # Нажатие кнопки мыши
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                # Если кликнули по верхней панели
                if mouse_pos[1] < CANVAS_Y:
                    handle_toolbar_click(mouse_pos)

                # Если кликнули по холсту
                elif in_canvas(mouse_pos):
                    pos = canvas_pos(mouse_pos)

                    # Заливка сразу выполняется по клику
                    if current_tool == "fill":
                        flood_fill(canvas, pos, current_color)

                    # Текстовый инструмент включает режим ввода
                    elif current_tool == "text":
                        text_mode = True
                        text_pos = pos
                        text_value = ""

                    # Остальные инструменты начинают рисование
                    else:
                        drawing = True
                        start_pos = pos
                        last_pos = pos

        # Движение мыши
        elif event.type == pygame.MOUSEMOTION:

            if drawing and in_canvas(mouse_pos):
                pos = canvas_pos(mouse_pos)

                # Карандаш рисует постоянно, пока мышь двигается
                if current_tool == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, pos, brush_size)
                    last_pos = pos

                # Ластик просто рисует белым цветом
                elif current_tool == "eraser":
                    pygame.draw.line(canvas, "white", last_pos, pos, brush_size)
                    last_pos = pos

        # Отпускание кнопки мыши
        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1 and drawing:
                end_pos = canvas_pos(mouse_pos)

                # Фигуры рисуются окончательно только после отпускания мыши
                if current_tool not in ("pencil", "eraser"):
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

    # Очищаем экран
    screen.fill("white")

    # Показываем холст
    screen.blit(canvas, (0, CANVAS_Y))

    # Живой предпросмотр линии и фигур
    # Мы рисуем фигуру на копии canvas, а не на самом canvas.
    if drawing and current_tool not in ("pencil", "eraser") and start_pos is not None:
        preview = canvas.copy()

        draw_shape(
            preview,
            current_tool,
            current_color,
            start_pos,
            canvas_mouse_pos,
            brush_size
        )

        screen.blit(preview, (0, CANVAS_Y))

    # Рисуем панель сверху
    draw_toolbar()

    # Показываем текст во время ввода
    draw_text_preview()

    # Обновляем окно
    pygame.display.flip()

    # Ограничиваем FPS
    clock.tick(60)

pygame.quit()