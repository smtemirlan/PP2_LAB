import pygame
import datetime
import math
import os


class MickeyClock:
    def __init__(self, screen):
        self.screen = screen
        self.center = (300, 300)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "images", "mickeyclock.jpeg")

        self.bg = pygame.image.load(image_path)
        self.bg = pygame.transform.scale(self.bg, (600, 600))

        self.seconds = 0
        self.minutes = 0

    def update(self):
        now = datetime.datetime.now()
        self.seconds = now.second
        self.minutes = now.minute

    def draw_hand(self, angle, length, color, width):
        rad = math.radians(angle - 90)

        x = self.center[0] + length * math.cos(rad)
        y = self.center[1] + length * math.sin(rad)

        pygame.draw.line(self.screen, color, self.center, (x, y), width)

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        sec_angle = (self.seconds / 60) * 360
        min_angle = (self.minutes / 60) * 360

        self.draw_hand(sec_angle, 180, (255, 0, 0), 3)
        self.draw_hand(min_angle, 130, (0, 0, 0), 6)

        pygame.draw.circle(self.screen, (0, 0, 0), self.center, 8)