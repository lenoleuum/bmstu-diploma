from midi2audio import FluidSynth
from pydub import AudioSegment
from pydub.playback import play
import os


class Transformer:
    def __init__(self):
        self.tmp_file = "tmp.wav"

    def midi_to_mp3(self, file_in:str, file_out:str):
        #fs = FluidSynth()
        #fs.sfload("C:\\ProgramData\\soundfonts\\default.sf2")
        FluidSynth().midi_to_audio(file_in, self.tmp_file)
        wav_file = AudioSegment.from_wav(self.tmp_file)
        wav_file.export(file_out, format="mp3")
        os.remove(self.tmp_file)

    def play_mp3(self, filepath:str):
        sound = AudioSegment.from_mp3(filepath)
        playback = play(sound)

        return playback
    
    def stop_mp3(self, playback):
        playback.stop()


    def normalize(self, file_in:str, file_out:str):
        mp3_file = AudioSegment.from_mp3(file_in)
        normalized_file = mp3_file.normalize()
        normalized_file.export(file_out, format="mp3")