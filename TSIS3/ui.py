import pygame

from racer import game_loop
from persistence import (
    load_settings,
    save_settings,
    load_leaderboard,
    add_score
)


WIDTH = 520
HEIGHT = 620


def draw_text(screen, text, size, x, y, color=(255, 255, 255), center=True):
    # Рисует текст
    font = pygame.font.SysFont("arial", size)
    image = font.render(text, True, color)
    rect = image.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(image, rect)


def draw_button(screen, rect, text, active=False):
    # Рисует кнопку
    color = (80, 120, 200) if active else (55, 55, 70)

    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, (230, 230, 230), rect, 2, border_radius=8)

    draw_text(screen, text, 24, rect.centerx, rect.centery)


def check_button(rect, event):
    # Проверяет клик
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and rect.collidepoint(event.pos)


def input_player_name(screen, clock):
    # Ввод имени игрока
    name = ""

    while True:
        screen.fill((20, 20, 30))

        draw_text(screen, "Enter your name", 36, WIDTH // 2, 160)
        draw_text(screen, name + "|", 30, WIDTH // 2, 250, (255, 230, 80))
        draw_text(screen, "Press Enter to start", 22, WIDTH // 2, 340, (180, 180, 180))
        draw_text(screen, "Esc - back", 20, WIDTH // 2, 380, (180, 180, 180))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name.strip() or "Player"

                if event.key == pygame.K_ESCAPE:
                    return None

                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                elif len(name) < 14 and event.unicode.isprintable():
                    name += event.unicode

        clock.tick(60)


def leaderboard_screen(screen, clock):
    # Экран лидеров
    while True:
        screen.fill((20, 20, 30))

        draw_text(screen, "TOP 10 LEADERBOARD", 34, WIDTH // 2, 55)

        scores = load_leaderboard()

        if not scores:
            draw_text(screen, "No scores yet", 26, WIDTH // 2, 180, (200, 200, 200))
        else:
            y = 115
            draw_text(screen, "Rank   Name        Score   Dist   Coins", 20, 50, y, (255, 230, 80), center=False)
            y += 35

            for index, item in enumerate(scores, start=1):
                row = f"{index:<4}  {item['name']:<10}  {item['score']:<6}  {item['distance']:<5}  {item['coins']}"
                draw_text(screen, row, 20, 50, y, (230, 230, 230), center=False)
                y += 32

        draw_text(screen, "Press Esc to return", 20, WIDTH // 2, HEIGHT - 45, (180, 180, 180))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True

        clock.tick(60)


def settings_screen(screen, clock, settings):
    # Экран настроек
    colors = ["blue", "black", "green"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        screen.fill((20, 20, 30))

        draw_text(screen, "SETTINGS", 38, WIDTH // 2, 55)

        sound_rect = pygame.Rect(110, 130, 300, 50)
        color_rect = pygame.Rect(110, 210, 300, 50)
        diff_rect = pygame.Rect(110, 290, 300, 50)
        back_rect = pygame.Rect(110, 430, 300, 50)

        draw_button(screen, sound_rect, f"Sound: {'ON' if settings['sound'] else 'OFF'}")
        draw_button(screen, color_rect, f"Car color: {settings['car_color']}")
        draw_button(screen, diff_rect, f"Difficulty: {settings['difficulty']}")
        draw_button(screen, back_rect, "Back")

        draw_text(screen, "Click button to change", 20, WIDTH // 2, 380, (180, 180, 180))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                return False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                save_settings(settings)
                return True

            if check_button(sound_rect, event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)

            if check_button(color_rect, event):
                i = colors.index(settings["car_color"])
                settings["car_color"] = colors[(i + 1) % len(colors)]
                save_settings(settings)

            if check_button(diff_rect, event):
                i = difficulties.index(settings["difficulty"])
                settings["difficulty"] = difficulties[(i + 1) % len(difficulties)]
                save_settings(settings)

            if check_button(back_rect, event):
                save_settings(settings)
                return True

        clock.tick(60)


def main_menu():
    # Главное меню
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS3 Racer Menu")
    clock = pygame.time.Clock()

    settings = load_settings()

    while True:
        screen.fill((20, 20, 30))

        draw_text(screen, "TSIS3 RACER", 44, WIDTH // 2, 90)
        draw_text(screen, "Advanced driving game", 22, WIDTH // 2, 130, (180, 180, 180))

        play_rect = pygame.Rect(140, 210, 240, 55)
        lead_rect = pygame.Rect(140, 285, 240, 55)
        settings_rect = pygame.Rect(140, 360, 240, 55)
        exit_rect = pygame.Rect(140, 435, 240, 55)

        draw_button(screen, play_rect, "Play")
        draw_button(screen, lead_rect, "Leaderboard")
        draw_button(screen, settings_rect, "Settings")
        draw_button(screen, exit_rect, "Exit")

        draw_text(screen, "Use mouse. Esc exits screens.", 18, WIDTH // 2, 555, (150, 150, 150))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if check_button(play_rect, event):
                player_name = input_player_name(screen, clock)

                if player_name:
                    result = game_loop(player_name, settings)

                    if result:
                        add_score(
                            player_name,
                            result["score"],
                            result["distance"],
                            result["coins"]
                        )

                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    pygame.display.set_caption("TSIS3 Racer Menu")

            if check_button(lead_rect, event):
                if not leaderboard_screen(screen, clock):
                    pygame.quit()
                    return

            if check_button(settings_rect, event):
                if not settings_screen(screen, clock, settings):
                    pygame.quit()
                    return

            if check_button(exit_rect, event):
                pygame.quit()
                return

        clock.tick(60)
