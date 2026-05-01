import random
from pathlib import Path

import pygame


BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"
SOUNDS_DIR = BASE_DIR / "sounds"

WIDTH = 400
HEIGHT = 600

ROAD_LEFT = 55
ROAD_RIGHT = 345

PLAYER_W = 45
PLAYER_H = 80

LANES = [95, 177, 260]


def load_image(name, size):
    # Загружает картинку
    path = IMAGES_DIR / name

    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)

    except Exception:
        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill((200, 0, 0))
        return surface


def load_sound(name):
    # Загружает звук
    path = SOUNDS_DIR / name

    try:
        return pygame.mixer.Sound(path)

    except Exception:
        return None


def start_background_music(settings):
    # Запускает музыку
    if not settings.get("sound", True):
        return

    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(SOUNDS_DIR / "background.wav")
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play(-1)

    except Exception as error:
        print("Background music error:", error)


def stop_background_music():
    # Останавливает музыку
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass


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


def choose_player_image(settings):
    # Выбирает машину
    color = settings.get("car_color", "blue")

    if color == "black":
        return "Player_Black.png"

    if color == "green":
        return "Player_Green.png"

    return "Player_Blue.png"


def difficulty_values(settings):
    # Настройки сложности
    difficulty = settings.get("difficulty", "normal")

    if difficulty == "easy":
        return 4, 1100

    if difficulty == "hard":
        return 7, 700

    return 5, 900


def make_enemy(enemy_img, speed):
    # Создаёт врага
    x = random.choice(LANES)
    y = random.randint(-650, -100)

    return {
        "type": "enemy",
        "image": enemy_img,
        "rect": pygame.Rect(x, y, 45, 80),
        "prev_rect": pygame.Rect(x, y, 45, 80),
        "speed": speed
    }


def make_oil(oil_img, speed):
    # Создаёт масло
    x = random.choice(LANES)
    y = random.randint(-700, -120)

    return {
        "type": "oil",
        "image": oil_img,
        "rect": pygame.Rect(x, y, 45, 45),
        "prev_rect": pygame.Rect(x, y, 45, 45),
        "speed": speed
    }


def make_power(power_images, speed):
    # Создаёт усиление
    power_type = random.choice(["nitro", "shield", "repair"])
    image = power_images[power_type]

    x = random.choice(LANES)
    y = random.randint(-900, -200)

    return {
        "type": power_type,
        "image": image,
        "rect": pygame.Rect(x, y, 38, 38),
        "prev_rect": pygame.Rect(x, y, 38, 38),
        "speed": speed
    }


def make_coin(speed):
    # Создаёт монету
    value = random.choice([1, 1, 1, 2, 2, 3])
    x = random.choice(LANES) + 20
    y = random.randint(-500, -50)

    return {
        "type": "coin",
        "value": value,
        "rect": pygame.Rect(x, y, 18, 18),
        "prev_rect": pygame.Rect(x, y, 18, 18),
        "speed": speed
    }


def safe_spawn(new_rect, objects):
    # Безопасное появление
    for obj in objects:
        if new_rect.colliderect(obj["rect"].inflate(35, 90)):
            return False

    return True


def check_collision(player_rect, object_rect, prev_rect=None):
    # Проверяет столкновение
    player_hitbox = player_rect.inflate(10, 10)
    object_hitbox = object_rect.inflate(18, 18)

    # Обычная проверка
    if player_hitbox.colliderect(object_hitbox):
        return True

    # Проверка проскока
    if prev_rect is not None:
        swept_rect = object_rect.union(prev_rect)
        swept_rect = swept_rect.inflate(18, 18)

        if player_hitbox.colliderect(swept_rect):
            return True

    return False


def show_game_over(screen, score, distance, coins):
    # Экран Game Over
    while True:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (240, 240, 240), (45, 170, 310, 240), border_radius=10)

        draw_text(screen, "GAME OVER", 34, WIDTH // 2, 205, (200, 0, 0))
        draw_text(screen, f"Score: {score}", 24, WIDTH // 2, 260, (0, 0, 0))
        draw_text(screen, f"Distance: {distance}", 24, WIDTH // 2, 295, (0, 0, 0))
        draw_text(screen, f"Coins: {coins}", 24, WIDTH // 2, 330, (0, 0, 0))
        draw_text(screen, "Enter - menu | R - retry", 19, WIDTH // 2, 375, (0, 0, 0))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "menu"

                if event.key == pygame.K_r:
                    return "retry"

                if event.key == pygame.K_ESCAPE:
                    return "menu"


def game_loop(player_name, settings):
    # Главная игра
    pygame.init()

    try:
        pygame.mixer.init()
    except Exception:
        pass

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS3 Racer")
    clock = pygame.time.Clock()

    bg_img = load_image("AnimatedStreet.png", (WIDTH, HEIGHT))
    player_img = load_image(choose_player_image(settings), (PLAYER_W, PLAYER_H))
    enemy_img = load_image("Enemy.png", (45, 80))
    oil_img = load_image("oil.png", (45, 45))

    power_images = {
        "nitro": load_image("Power1.png", (38, 38)),
        "shield": load_image("Shield.png", (38, 38)),
        "repair": load_image("Repair.png", (38, 38))
    }

    crash_sound = load_sound("crash.wav")

    while True:
        start_background_music(settings)

        base_enemy_speed, spawn_delay = difficulty_values(settings)

        player = pygame.Rect(WIDTH // 2 - PLAYER_W // 2, HEIGHT - 105, PLAYER_W, PLAYER_H)
        player_speed = 5

        enemies = [make_enemy(enemy_img, base_enemy_speed)]
        oils = [make_oil(oil_img, base_enemy_speed - 1)]
        powers = [make_power(power_images, base_enemy_speed - 1)]
        coins = [make_coin(base_enemy_speed - 1)]

        score = 0
        coin_sum = 0
        distance = 0

        shield = False
        repairs = 0
        active_power = "none"
        active_until = 0

        slow_until = 0
        last_spawn = pygame.time.get_ticks()
        start_time = pygame.time.get_ticks()

        running = True
        game_over = False

        while running:
            now = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_background_music()
                    return None

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    stop_background_music()
                    return {
                        "score": score,
                        "distance": distance,
                        "coins": coin_sum
                    }

            keys = pygame.key.get_pressed()

            current_speed = player_speed

            if now < active_until and active_power == "nitro":
                current_speed = 8

            if now < slow_until:
                current_speed = 3

            if now >= active_until and active_power == "nitro":
                active_power = "none"

            if keys[pygame.K_LEFT] and player.left > ROAD_LEFT + 5:
                player.x -= current_speed

            if keys[pygame.K_RIGHT] and player.right < ROAD_RIGHT - 5:
                player.x += current_speed

            if keys[pygame.K_UP] and player.top > 0:
                player.y -= current_speed

            if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
                player.y += current_speed

            distance = (now - start_time) // 100
            difficulty_bonus = distance // 120
            object_speed = base_enemy_speed + difficulty_bonus

            if now - last_spawn > max(350, spawn_delay - difficulty_bonus * 30):
                new_choice = random.choice(["enemy", "enemy", "oil", "coin", "power"])

                if new_choice == "enemy":
                    obj = make_enemy(enemy_img, object_speed)

                    if safe_spawn(obj["rect"], enemies + oils + powers + coins):
                        enemies.append(obj)

                elif new_choice == "oil":
                    obj = make_oil(oil_img, object_speed - 1)

                    if safe_spawn(obj["rect"], enemies + oils + powers + coins):
                        oils.append(obj)

                elif new_choice == "coin":
                    obj = make_coin(object_speed - 1)

                    if safe_spawn(obj["rect"], enemies + oils + powers + coins):
                        coins.append(obj)

                else:
                    obj = make_power(power_images, object_speed - 1)

                    if safe_spawn(obj["rect"], enemies + oils + powers + coins):
                        powers.append(obj)

                last_spawn = now

            # Движение объектов
            for group in [enemies, oils, powers, coins]:
                for obj in group[:]:
                    obj["prev_rect"] = obj["rect"].copy()
                    obj["rect"].y += obj["speed"]

                    if obj["rect"].top > HEIGHT:
                        group.remove(obj)

            # Столкновение с врагом
            for enemy in enemies[:]:
                if check_collision(player, enemy["rect"], enemy.get("prev_rect")):
                    if shield:
                        shield = False
                        active_power = "none"
                        enemies.remove(enemy)

                    elif repairs > 0:
                        repairs -= 1
                        enemies.remove(enemy)

                    else:
                        stop_background_music()

                        if settings.get("sound", True) and crash_sound:
                            crash_sound.play()

                        game_over = True
                        break

            # Остальное проверяем только если игра не закончилась
            if not game_over:

                # Столкновение с маслом
                for oil in oils[:]:
                    if check_collision(player, oil["rect"], oil.get("prev_rect")):

                        if shield:
                            shield = False
                            active_power = "none"
                            oils.remove(oil)

                        elif repairs > 0:
                            repairs -= 1
                            oils.remove(oil)

                        else:
                            slow_until = now + 2500
                            oils.remove(oil)

                # Сбор монет
                for coin in coins[:]:
                    if check_collision(player, coin["rect"], coin.get("prev_rect")):
                        coin_sum += coin["value"]
                        score += coin["value"] * 10
                        coins.remove(coin)

                # Сбор усилений
                for power in powers[:]:
                    if check_collision(player, power["rect"], power.get("prev_rect")):
                        if power["type"] == "nitro":
                            active_power = "nitro"
                            active_until = now + 4000

                        elif power["type"] == "shield":
                            shield = True
                            active_power = "shield"

                        elif power["type"] == "repair":
                            repairs = min(1, repairs + 1)
                            active_power = "repair"

                        powers.remove(power)

            score = distance + coin_sum * 10

            screen.blit(bg_img, (0, 0))

            pygame.draw.line(screen, (255, 255, 255), (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 3)
            pygame.draw.line(screen, (255, 255, 255), (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 3)

            for obj in enemies:
                screen.blit(obj["image"], obj["rect"])

            for obj in oils:
                screen.blit(obj["image"], obj["rect"])

            for obj in powers:
                screen.blit(obj["image"], obj["rect"])

            for coin in coins:
                color = (255, 220, 0) if coin["value"] == 1 else (255, 150, 0)

                pygame.draw.circle(screen, color, coin["rect"].center, coin["rect"].width // 2)
                pygame.draw.circle(screen, (0, 0, 0), coin["rect"].center, coin["rect"].width // 2, 2)

                draw_text(screen, str(coin["value"]), 14, coin["rect"].centerx, coin["rect"].centery, (0, 0, 0))

            screen.blit(player_img, player)

            if shield:
                pygame.draw.circle(screen, (80, 170, 255), player.center, 48, 3)

            draw_text(screen, f"Player: {player_name}", 17, 10, 10, (0, 0, 0), center=False)
            draw_text(screen, f"Score: {score}", 17, 10, 32, (0, 0, 0), center=False)
            draw_text(screen, f"Distance: {distance}", 17, 10, 54, (0, 0, 0), center=False)
            draw_text(screen, f"Coins: {coin_sum}", 17, 10, 76, (0, 0, 0), center=False)

            if active_power != "none":
                if active_power == "nitro":
                    left = max(0, (active_until - now) // 1000)
                    text = f"Power: Nitro {left}s"

                elif active_power == "shield":
                    text = "Power: Shield"

                else:
                    text = f"Repair: {repairs}"

                draw_text(screen, text, 17, 10, 98, (0, 0, 0), center=False)

            if now < slow_until:
                draw_text(screen, "Oil slow!", 20, WIDTH // 2, 40, (180, 0, 0))

            pygame.display.flip()
            clock.tick(60)

            if game_over:
                action = show_game_over(screen, score, distance, coin_sum)

                if action == "retry":
                    running = False

                elif action == "quit":
                    stop_background_music()
                    return None

                else:
                    stop_background_music()

                    return {
                        "score": score,
                        "distance": distance,
                        "coins": coin_sum
                    }