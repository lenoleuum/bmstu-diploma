from music21 import note, instrument, stream, tempo, midi, chord, meter
from midi2audio import FluidSynth

import sys
sys.path.append('..')

from constants.Constants import DefaultMidiFile

def create_midi_file(notes:list, time_signature:str='4/4', bpm:int=120, file:str=DefaultMidiFile):
    result = []
    offset = 0

    result.append(meter.TimeSignature(time_signature))
    result.append(tempo.MetronomeMark(bpm))

    for n in notes:
        if len(n[0]) == 1:
            new_note = note.Note(int(n[0]))
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()

            result.append(new_note)
        else:
            n_chord = []
            for c in n[0].split(' '):
                n_chord.append(note.Note(int(c)))

            new_chord = chord.Chord(n_chord)
            new_chord.offset = offset
            new_chord.storedInstrument = instrument.Piano()

            result.append(new_chord)

        offset += float(n[1])

    midi_stream = stream.Stream(result)
    midi_stream.write('midi', fp=file)

def play_midi(midi_path:str):
    FluidSynth().play_midi(midi_path)