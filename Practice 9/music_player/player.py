import pygame
import os


class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()

        base_dir = os.path.dirname(os.path.abspath(__file__))

        self.playlist = [
            os.path.join(base_dir, "music", "track1.wav"),
            os.path.join(base_dir, "music", "track2.wav")
        ]

        self.current_index = 0
        self.is_playing = False

    def play(self):
        pygame.mixer.music.load(self.playlist[self.current_index])
        pygame.mixer.music.play()
        self.is_playing = True
    
    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def prev(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    def get_current_track(self):
        return os.path.basename(self.playlist[self.current_index])
    
    def get_position(self):
        pos = pygame.mixer.music.get_pos()
        return pos // 1000