import shutil
from pathlib import Path
import os

from constants.Constants import Constants
from .Parser import Parser


class Classificator:
    def __init__(self):
        self.parser = Parser(Constants.TracksPath)

    def extract_tonalities(self, midi_part):
        dict = {}
        for chorale in midi_part:
            key = chorale.analyze('key').tonicPitchNameWithCase
            dict[key] = dict[key] + 1 if key in dict.keys() else 1

        return dict
    

    def define_main_tonality(self, tonalities:dict):
        return max(tonalities, key=tonalities.get)

    def define_color(self, tonality:str):
        for key in Constants.TonalititesToColors.keys():
            if tonality.lower() in Constants.TonalititesToColors[key]:
                return key
            
    def define_lad(self, tonality:str):
        if tonality.isupper():
            return 'major'
        else:
            return 'minor'

    def classify(self):
        data = []
        self.parser.walk_directory(data, Constants.TracksPath)

        self.clear_color_folders()

        print("[classify]")

        for dir in data:
            for file in dir:
                midi_part = self.parser.open_midi_file(file, True)
                tonalitites = self.extract_tonalities(midi_part)
                main_tonality = self.define_main_tonality(tonalitites)
                color = self.define_color(main_tonality)
                lad = self.define_lad(main_tonality)

                if color is None:
                    continue

                for key in Constants.ColorsPathDict.keys():
                    if color == key:
                        shutil.copy(file, Constants.ColorsPathDict[key] + "\\" + lad)

                print(file, color.upper(), lad)

        print("DONE")

    def clear_color_folders(self):
        for key in Constants.ColorsPathDict.keys():
                for lad in Constants.Lads:
                    path = Constants.ColorsPathDict[key] + "\\" + lad
                    [f.unlink() for f in Path(path).glob("*") if f.is_file()] 



#c = Classificator()
#c.classify()