import datetime
from music21 import note, instrument, stream, tempo, midi, chord, meter
from midi2audio import FluidSynth

import sys
sys.path.append('..')

from constants.Constants import Constants

class Converter:
    def __init__(self):
        pass

    def convert(self, data:list, meta:dict, filename:str=None):
        result = []
        offset = 0

        result.append(meter.TimeSignature(meta['time_signature']))
        result.append(tempo.MetronomeMark(meta['bpm']))

        for el in data:
            if type(el[0]) is int:
                new_note = note.Note(int(el[0]))
                new_note.offset = offset
                new_note.storedInstrument = instrument.Piano()

                result.append(new_note)
            else:
                n_chord = []
                for c in el[0]:
                    n_chord.append(note.Note(int(c)))

                new_chord = chord.Chord(n_chord)
                new_chord.offset = offset
                new_chord.storedInstrument = instrument.Piano()

                result.append(new_chord)

            offset += float(el[1])

        midi_stream = stream.Stream(result)

        if filename is None:
            filename = self.build_file_name()

        midi_stream.write('midi', fp=filename)   

        return filename

    def play(self, path:str):
        try:
            FluidSynth().play_midi(path)
        except:
            return

    @staticmethod
    def build_file_name():
        filename = Constants.WorkDir + "\\" + str(datetime.datetime.now()).split('.')[0].replace(':', '-') + ".mid"

        return filename