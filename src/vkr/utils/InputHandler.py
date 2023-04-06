import sys
sys.path.append("..")


from constants.Constants import Constants

class InputHandler:
    def __init__(self):
        pass

    def check_base_colors(self, colors:list):
        cnt = 0

        for i in range(len(colors)):
            if colors[i] in Constants.MainColors and i < 4:
                cnt += 1

        return cnt == Constants.MainColorsNum


    def get_dominant_color(self, colors:list):
        return colors[0]


    def get_rejected_color(self, colors:list):
        for col in reversed(colors):
            if col in Constants.MainColors:
                return col


    def handle(self, colors:list):
        meta = dict()
        if self.check_base_colors(colors):
            meta['bpm'] = 140
            meta['time_signature'] = '4/4'
            lad, tonica_color = Constants.Lads[0], self.get_dominant_color(colors)
            meta['lad'] = lad
            meta['color'] = tonica_color
        else:
            meta['bpm'] = 100
            meta['time_signature'] = '3/4'
            lad, tonica_color = Constants.Lads[1], self.get_rejected_color(colors)
            meta['lad'] = lad
            meta['color'] = tonica_color

        return meta
