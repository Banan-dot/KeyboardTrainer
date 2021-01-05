import pygame
import sys
import os


class Loader:
    @staticmethod
    def load_music(filename, volume):
        pygame.mixer.music.load('./Music/{}.mp3'.format(filename))
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(volume)

    @staticmethod
    def load_text(filename):
        text = []
        count_symbols = 0
        if os.path.exists(filename):
            with open(filename, encoding="utf8") as f:
                for line in f:
                    count_symbols += len(line)
                    text.append(line)
        else:
            print("File doesn't exist")
            quit()
        return text, count_symbols
