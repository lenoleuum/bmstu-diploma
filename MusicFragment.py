import time

import numpy as np
import simpleaudio as sa
import random

import Constants as const

from Tonality import Tonality


class MusicFragment:
    def __init__(self, notes):
        self.notes = notes

    # todo: проверить частоты - норм все
    @staticmethod
    def play(note, fs=8000, duration=0.5, volume=1):
        ns = np.arange(-9, 3)
        frequencies = 440 * 2 ** (ns / 12)
        note_names = const.Gamma
        Notes = {note_names[i]: frequencies[i] for i in range(ns.size)}

        t = np.linspace(0, duration, int(duration * fs), False)
        if note != 'O':
            if note[1:] != '' and note[1:] != '#':
                octave = int(note[-1])
                frequency = Notes[note[:-1]]
                frequency = frequency * 2 ** (octave - 4)
            else:
                frequency = Notes[note]
            audio = np.sin(2 * np.pi * frequency * t)
            audio = audio * (2 ** 15 - 1) / np.max(np.abs(audio))
        else:
            audio = np.zeros(int(duration * fs))
        audio = volume * audio
        audio = audio.astype(np.int16)
        play_object = sa.play_buffer(audio, 1, 2, fs)

    def play_music_fragment(self):
        for note in self.notes:
            self.play(note)
            time.sleep(0.5)
