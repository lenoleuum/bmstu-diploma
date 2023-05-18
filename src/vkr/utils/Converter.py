import datetime
import os
from music21 import note, instrument, stream, tempo, midi, chord, meter, volume
from midi2audio import FluidSynth
import random
import fluidsynth
from pydub import AudioSegment

import sys
sys.path.append('..')

from constants.Constants import Constants

class Converter:
    def __init__(self):
        pass

    @staticmethod
    def bar_length(numerator: int, denominator: int):
        return numerator * 1 / denominator

    def convert(self, data:list, meta:dict, filename:str=None):
        result = []
        offset = 0

        res_stream = stream.Stream()

        result.append(meter.TimeSignature(meta['time_signature']))
        result.append(tempo.MetronomeMark(meta['bpm']))
        numerator, denominator = int(meta['time_signature'].split('/')[0]), int(meta['time_signature'].split('/')[1])

        for el in data:

            if type(el[0]) is int:
                new_note = note.Note(int(el[0]))
                new_note.offset = offset
                new_note.storedInstrument = instrument.Piano()

                res_stream.append(new_note)
            else:
                n_chord = []
                for c in el[0]:
                    n_chord.append(note.Note(int(c)))

                new_chord = chord.Chord(n_chord)
                new_chord.offset = offset
                new_chord.storedInstrument = instrument.Piano()

                res_stream.append(new_chord)

            offset += float(el[1])  

        res_tempo = tempo.MetronomeMark(number = int(meta['bpm']))
        res_stream.insert(0, res_tempo)

        midi_stream = stream.Stream(result)

        folder = self.create_samples_dir()

        if filename is None:
            filename = self.build_file_name(folder, meta)

        res_stream.write('midi', fp=filename)  

        print(filename)

        return filename

    def play_midi(self, path:str):
        try:
            FluidSynth().play_midi(path)
        except:
            return
        
    def stop_midi(self):
        fs = fluidsynth.Synth()
        fs.stop()

    @staticmethod
    def create_samples_dir():
        folder_name = os.path.split(Constants.WorkDir)[0] + "\\samples\\" + str(datetime.date.today())

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        return folder_name

    @staticmethod
    def build_file_name(folder:str, meta:dict=None):
        filename = folder + "\\" + str(datetime.datetime.now()).split('.')[0].replace(':', '-') + " " + meta['color'] + " " + meta['lad'] + ".mid"

        return filename