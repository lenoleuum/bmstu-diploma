import Constants as const
from MusicFragment import MusicFragment
from Tonality import Tonality


def check_base_colors(colors):
    cnt = 0

    for i in range(len(colors)):
        if colors[i] in const.MainColors and i <= 4:
            cnt += 1

    return cnt == const.MainColorsNum


def get_dominant_color(colors):
    return colors[0]


def get_rejected_color(colors):
    for col in reversed(colors):
        if col in const.MainColors:
            return col


def process_input(colors):
    if check_base_colors(colors):
        lad, tonica_color = const.Major, get_dominant_color(colors)
    else:
        lad, tonica_color = const.Minor, get_rejected_color(colors)

    tonica = const.MainColorsToNotes.get(tonica_color)
    tonality = Tonality(lad, tonica)

    return lad, tonica, tonality.linked_list_to_list()


def translate_note(note):
    return const.GammaTranslated.get(note)


def translate_lad(lad):
    if lad == const.Major:
        return const.MajorTranslated
    else:
        return const.MinorTranslated
