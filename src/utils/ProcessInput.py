import sys
sys.path.append("..")


from constants.Constants import MainColors, MainColorsNum, Major, Minor, MainColorsToNotes, GammaTranslated, MajorTranslated, MinorTranslated
from music.Tonality import Tonality


def check_base_colors(colors):
    cnt = 0

    for i in range(len(colors)):
        if colors[i] in MainColors and i <= 4:
            cnt += 1

    return cnt == MainColorsNum


def get_dominant_color(colors):
    return colors[0]


def get_rejected_color(colors):
    for col in reversed(colors):
        if col in MainColors:
            return col


def process_input(colors):
    if check_base_colors(colors):
        lad, tonica_color = Major, get_dominant_color(colors)
    else:
        lad, tonica_color = Minor, get_rejected_color(colors)

    tonica = MainColorsToNotes.get(tonica_color)
    tonality = Tonality(lad, tonica)

    return lad, tonica, tonality.linked_list_to_list()


def translate_note(note):
    return GammaTranslated.get(note)


def translate_lad(lad):
    if lad == Major:
        return MajorTranslated
    else:
        return MinorTranslated
