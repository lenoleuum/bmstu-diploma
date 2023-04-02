import shutil

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


    def define_color(self, tonalities:dict):
        max_tonality = max(tonalities, key=tonalities.get)

        for key in Constants.TonalititesToColors.keys():
            if max_tonality.lower() in Constants.TonalititesToColors[key]:
                return key


    def classify(self):
        data = []
        self.parser.walk_directory(data, Constants.TracksPath)

        print("[classify]")

        for dir in data:
            for file in dir:
                midi_part = self.parser.open_midi_file(file, True)
                tonalitites = self.extract_tonalities(midi_part)
                color = self.define_color(tonalitites)

                if color is None:
                    continue

                for key in Constants.ColorsPathDict.keys():
                    if color == key:
                        shutil.copy(file, Constants.ColorsPathDict[key])

                print(file, color.upper())

        print("DONE")

    #def clear_color_folders(self):


c = Classificator()
#c.classify()