import json
from pathlib import Path

import pygame

from db import get_top, init_db, save_result
from game import HEIGHT, WIDTH, play_game


SETTINGS_FILE = Path(__file__).parent / "settings.json"


def load_settings():
    # Загружает настройки
    default = {
        "snake_color": [0, 180, 80],
        "grid": True,
        "sound": True
    }

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return default


def save_settings(settings):
    # Сохраняет настройки
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


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


def button(screen, text, rect, mouse_pos):
    # Рисует кнопку
    color = (70, 80, 100)

    if rect.collidepoint(mouse_pos):
        color = (95, 110, 140)

    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, (180, 180, 190), rect, 2, border_radius=8)

    draw_text(screen, text, 24, rect.centerx, rect.centery)

    return rect


def main_menu(screen, settings):
    # Главное меню
    username = "Player"
    active_input = False
    clock = pygame.time.Clock()

    while True:
        mouse_pos = pygame.mouse.get_pos()

        play_rect = pygame.Rect(200, 220, 200, 50)
        leaders_rect = pygame.Rect(200, 285, 200, 50)
        settings_rect = pygame.Rect(200, 350, 200, 50)
        exit_rect = pygame.Rect(200, 415, 200, 50)
        input_rect = pygame.Rect(170, 150, 260, 42)

        screen.fill((20, 25, 30))

        draw_text(screen, "TSIS4 Snake", 44, WIDTH // 2, 70)
        draw_text(screen, "Username:", 22, WIDTH // 2, 125)

        input_color = (80, 90, 120) if active_input else (55, 60, 75)
        pygame.draw.rect(screen, input_color, input_rect, border_radius=7)
        pygame.draw.rect(screen, (180, 180, 190), input_rect, 2, border_radius=7)
        draw_text(screen, username, 24, input_rect.centerx, input_rect.centery)

        button(screen, "Play", play_rect, mouse_pos)
        button(screen, "Leaderboard", leaders_rect, mouse_pos)
        button(screen, "Settings", settings_rect, mouse_pos)
        button(screen, "Exit", exit_rect, mouse_pos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit", username

            if event.type == pygame.MOUSEBUTTONDOWN:
                active_input = input_rect.collidepoint(event.pos)

                if play_rect.collidepoint(event.pos):
                    return "play", username.strip() or "Player"

                if leaders_rect.collidepoint(event.pos):
                    return "leaderboard", username

                if settings_rect.collidepoint(event.pos):
                    return "settings", username

                if exit_rect.collidepoint(event.pos):
                    return "exit", username

            if event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                elif event.key == pygame.K_RETURN:
                    active_input = False

                elif len(username) < 16:
                    username += event.unicode

        clock.tick(60)


def leaderboard_screen(screen):
    # Экран топ-10
    clock = pygame.time.Clock()
    rows = get_top(10)

    while True:
        screen.fill((18, 20, 28))
        draw_text(screen, "Leaderboard TOP-10", 38, WIDTH // 2, 55)

        if not rows:
            draw_text(screen, "No results or database is not connected", 23, WIDTH // 2, 180)
        else:
            y = 120

            for index, row in enumerate(rows, start=1):
                username, score, level, played_at = row
                line = f"{index}. {username} | score: {score} | level: {level}"
                draw_text(screen, line, 23, 80, y, center=False)
                y += 38

        draw_text(screen, "Press ESC to go back", 22, WIDTH // 2, 550)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        clock.tick(60)


def settings_screen(screen, settings):
    # Экран настроек
    clock = pygame.time.Clock()

    colors = [
        [0, 180, 80],
        [0, 120, 255],
        [230, 70, 70],
        [230, 220, 60]
    ]

    color_index = 0

    if settings.get("snake_color") in colors:
        color_index = colors.index(settings["snake_color"])

    while True:
        mouse_pos = pygame.mouse.get_pos()

        color_rect = pygame.Rect(160, 170, 280, 50)
        grid_rect = pygame.Rect(160, 240, 280, 50)
        sound_rect = pygame.Rect(160, 310, 280, 50)
        save_rect = pygame.Rect(160, 420, 280, 50)

        screen.fill((20, 25, 30))
        draw_text(screen, "Settings", 42, WIDTH // 2, 70)

        button(screen, f"Snake color: {color_index + 1}", color_rect, mouse_pos)
        button(screen, f"Grid: {settings.get('grid', True)}", grid_rect, mouse_pos)
        button(screen, f"Sound: {settings.get('sound', True)}", sound_rect, mouse_pos)
        button(screen, "Save and back", save_rect, mouse_pos)

        pygame.draw.rect(screen, tuple(colors[color_index]), (455, 175, 40, 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                save_settings(settings)
                return "menu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if color_rect.collidepoint(event.pos):
                    color_index = (color_index + 1) % len(colors)
                    settings["snake_color"] = colors[color_index]

                if grid_rect.collidepoint(event.pos):
                    settings["grid"] = not settings.get("grid", True)

                if sound_rect.collidepoint(event.pos):
                    settings["sound"] = not settings.get("sound", True)

                if save_rect.collidepoint(event.pos):
                    save_settings(settings)
                    return "menu"

        clock.tick(60)


def game_over_screen(screen, username, result):
    # Экран окончания игры
    clock = pygame.time.Clock()
    score = result["score"]
    level = result["level"]

    save_result(username, score, level)

    while True:
        mouse_pos = pygame.mouse.get_pos()

        again_rect = pygame.Rect(180, 330, 240, 50)
        menu_rect = pygame.Rect(180, 400, 240, 50)

        screen.fill((25, 20, 25))

        draw_text(screen, "GAME OVER", 48, WIDTH // 2, 110, (230, 70, 70))
        draw_text(screen, f"Player: {username}", 26, WIDTH // 2, 190)
        draw_text(screen, f"Score: {score}", 28, WIDTH // 2, 235)
        draw_text(screen, f"Level: {level}", 28, WIDTH // 2, 275)

        button(screen, "Play again", again_rect, mouse_pos)
        button(screen, "Main menu", menu_rect, mouse_pos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if again_rect.collidepoint(event.pos):
                    return "again"

                if menu_rect.collidepoint(event.pos):
                    return "menu"

        clock.tick(60)


def main():
    # Запуск программы
    pygame.init()

    init_db()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS4 Snake")

    settings = load_settings()
    username = "Player"

    while True:
        action, username = main_menu(screen, settings)

        if action == "exit":
            break

        if action == "leaderboard":
            result = leaderboard_screen(screen)

            if result == "exit":
                break

        if action == "settings":
            result = settings_screen(screen, settings)

            if result == "exit":
                break

        if action == "play":
            result = play_game(screen, username, settings)

            if result is None:
                continue

            next_action = game_over_screen(screen, username, result)

            if next_action == "exit":
                break

            while next_action == "again":
                result = play_game(screen, username, settings)

                if result is None:
                    break

                next_action = game_over_screen(screen, username, result)

                if next_action == "exit":
                    pygame.quit()
                    return

    pygame.quit()


if __name__ == "__main__":
    main()
