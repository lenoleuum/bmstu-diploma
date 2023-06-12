import pygame
import threading
import os
import time


class Player(threading.Thread):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.running = True

    def run(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy() and self.running:
            continue

        pygame.mixer.music.stop()

        '''pygame.mixer.music.fadeout(1000)
        file = None
        try:
            file = open("playing.mp3", 'r')
            file.close()
        except Exception as e:
            print(e)

        time.sleep(1)'''
        #os.remove("playing.mp3")

    def stop(self):
        self.running = False