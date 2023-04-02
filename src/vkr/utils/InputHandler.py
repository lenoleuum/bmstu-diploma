import sys
sys.path.append("..")


from constants.Constants import MainColors, MainColorsNum, Major, Minor, MainColorsToNotes, GammaTranslated, MajorTranslated, MinorTranslated

class InputHandler:
    def __init__(self):
        pass

    def check_base_colors(self, colors:list):
        cnt = 0

        for i in range(len(colors)):
            if colors[i] in MainColors and i <= 4:
                cnt += 1

        return cnt == MainColorsNum


    def get_dominant_color(self, colors:list):
        return colors[0]


    def get_rejected_color(self, colors:list):
        for col in reversed(colors):
            if col in MainColors:
                return col


    def handle(self, colors:list):
        meta = dict()
        if self.check_base_colors(colors):
            meta['bpm'] = 140
            meta['time_signature'] = '4/4'
            lad, tonica_color = Major, self.get_dominant_color(colors)
        else:
            meta['bpm'] = 100
            meta['time_signature'] = '3/4'
            lad, tonica_color = Minor, self.get_rejected_color(colors)

        return meta, tonica_color
