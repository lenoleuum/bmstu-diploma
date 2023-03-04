import math

import mido
import Constants as const
from midi2audio import FluidSynth


class MidiFileMeta:
    def __init__(self, file_path):
        self.path = file_path
        self.sf2_path = const.SF2Path

# todo: разобраться с этим
class MidiFile:
    def __init__(self, file_path):
        self.meta = MidiFileMeta(file_path)
        self.file = mido.MidiFile()
        #self.file.type = 0

    # channel=0 - перкуссия, а все остальные - фортепиано
    @staticmethod
    def note_on(track, note, velocity=120, time=100):
        track.append(mido.Message('note_on', note=note, velocity=velocity, time=time))

    @staticmethod
    def note_off(track, note, velocity=64, time=100):
        track.append(mido.Message('note_off', note=note, velocity=velocity, time=time))

    @staticmethod
    def convert_note(note):
        key = note[:-1]
        octave = note[-1]
        midi_number = -1

        if not octave.isdigit():
            key = note
            octave = '4'

        try:
            if 'b' in key:
                pos = const.GammaBb.index(key)
            else:
                pos = const.GammaDies.index(key)
        except:
            return None

        midi_number += pos + 12 * (int(octave) + 1) + 1

        return midi_number

    @staticmethod
    def frequency_to_note(frequency):
        C0 = const.A4 * pow(2, -4.75)
        h = round(12 * math.log2(frequency / C0))
        octave = h // 12
        n = h % 12
        return const.GammaDies[n] + str(octave)

    @staticmethod
    def get_frequency(note):
        return math.pow(2, (int(note) - 69) / 12) * const.A4

    def add_track(self, notes):
        track = mido.MidiTrack()
        track.append(mido.Message('program_change', program=12, time=0))

        for n in notes:
            note = self.convert_note(n)
            self.note_on(track, note)
            self.note_off(track, note)

        self.file.tracks.append(track)

    def get_tracks(self):
        return self.file.tracks

    def save_midi_file(self):
        self.file.save(self.meta.path)

    def download_midi_file(self, path):
        self.file.save(path)

    def play(self):
        FluidSynth().play_midi(self.meta.path)

    def parse(self):
        self.file = mido.MidiFile(self.meta.path)
        notes = [[] for i in range(16)]

        for track in self.file.tracks:
            for msg in track:#sorted(track, key=lambda s: s.time):
                if msg.type in ['note_on', 'note_off']:
                    notes[msg.channel].append(msg.note)

        bigram_notes = []

        for n in notes:
            for i in range(len(n) - 1):
                note_cur = self.frequency_to_note(self.get_frequency(n[i]))
                note_next = self.frequency_to_note(self.get_frequency(n[i + 1]))
                bigram_notes.append(note_cur + ' ' + note_next)

        return bigram_notes

    def parse_with_time(self):
        self.file = mido.MidiFile(self.meta.path)
        notes = [[] for i in range(16)]

        for track in self.file.tracks:
            for msg in track:#sorted(track, key=lambda s: s.time):
                if msg.type in ['note_on', 'note_off']:
                    notes[msg.channel].append(msg.note)
                    print(msg)

        bigram_notes = []

        for n in notes:
            for i in range(len(n) - 1):
                note_cur = self.frequency_to_note(self.get_frequency(n[i]))
                note_next = self.frequency_to_note(self.get_frequency(n[i + 1]))
                bigram_notes.append(note_cur + ' ' + note_next)

        return bigram_notes

# kuznechik.mid CrazyFrog.mid Fur Elise.mid rasputin.mid
m = MidiFile("C:\\Users\\admin\\Desktop\\newlife\\8 semester\\в последний путь\\midi\\kuznechik.mid")
print(m.file.length)
#m.play()