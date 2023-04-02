class Constants:
    # ui consts
    WindowColor = 'white'
    AdditionalColor = 'gold'


    WorkDir = r"C:\Users\admin\Desktop\newlife\8 semester\в последний путь\VKR\samples"

    ColorsDict = dict({'blue': 'Blue',
                   'green': 'Lime',
                   'red': 'Red',
                   'yellow': 'Yellow',
                   'purple': 'DarkMagenta',
                   'black': 'Black',
                   'grey': 'Gray',
                   'brown': 'SaddleBrown'})
    Colors = ['blue', 'green', 'red', 'yellow', 'purple', 'black', 'grey', 'brown']

    MainColorsNum = 4
    ColorsNum = 8
    MainColors = ['blue', 'green', 'red', 'yellow']

    # classificator consts
    TonalititesToColors = dict({'red': ['f#', 'f', 'g'],
                            'yellow': ['a', 'b#', 'g#'],
                            'green': ['b', 'c', 'c#'],
                            'blue': ['d', 'd#', 'e']})


    ColorsPathDict = dict({'red': r"C:\Users\admin\Desktop\newlife\8 semester\в последний путь\VKR\training data\colors\red",
                        'blue': r"C:\Users\admin\Desktop\newlife\8 semester\в последний путь\VKR\training data\colors\blue",
                        'green': r"C:\Users\admin\Desktop\newlife\8 semester\в последний путь\VKR\training data\colors\green",
                        'yellow': r"C:\Users\admin\Desktop\newlife\8 semester\в последний путь\VKR\training data\colors\yellow"})

    ColorsPath = r"C:\Users\admin\Desktop\newlife\8 semester\в последний путь\VKR\training data\colors"

    TracksPath = r"C:\Users\admin\Desktop\newlife\8 semester\в последний путь\VKR\training data\tracks"


Major = 'major'
Minor = 'minor'
MajorTranslated = 'Мажор'
MinorTranslated = 'Минор'
MajorLad = [1, 1, 0.5, 1, 1, 1, 0.5]
MinorLad = [1, 0.5, 1, 1, 0.5, 1, 1]

KeyBoardDies = ['A0', 'B0', 'A#0',
                'C1', 'C#1', 'D1', 'D#1', 'E1', 'F1', 'F#1', 'G1', 'G#1', 'A1', 'A#1', 'B1',
                'C2', 'C#2', 'D2', 'D#2', 'E2', 'F2', 'F#2', 'G2', 'G#2', 'A2', 'A#2', 'B2',
                'C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3',
                'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4',
                'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'B5',
                'C6', 'C#6', 'D6', 'D#6', 'E6', 'F6', 'F#6', 'G6', 'G#6', 'A6', 'A#6', 'B6',
                'C7', 'C#7', 'D7', 'D#7', 'E7', 'F7', 'F#7', 'G7', 'G#7', 'A7', 'A#7', 'B7',
                'C8']

Gamma = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

GammaDies = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
GammaBb = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

GammaTranslated = dict({'C': 'До',
                        'C#': 'До Диез',
                        'D': 'Ре',
                        'D#': 'Ре Диез',
                        'E': 'Ми',
                        'F': 'Фа',
                        'F#': 'Фа Диез',
                        'G': 'Соль',
                        'G#': 'Соль Диез',
                        'A': 'Ля',
                        'A#': 'Ля Диез',
                        'B': 'Си'})

# Си бемоль и ля диез это вроде одно и то же? - это взаимозаменяемо?
MainColorsNum = 4
ColorsNum = 8
MainColors = ['blue', 'green', 'red', 'yellow']
MainColorsToNotes = dict({'blue': 'D', 'green': 'C', 'red': 'F#', 'yellow': 'A#'})

WindowColor = 'white'
AdditionalColor = 'gold'
ColorsDict = dict({'blue': 'Blue',
                   'green': 'Lime',
                   'red': 'Red',
                   'yellow': 'Yellow',
                   'purple': 'DarkMagenta',
                   'black': 'Black',
                   'grey': 'Gray',
                   'brown': 'SaddleBrown'})
Colors = ['blue', 'green', 'red', 'yellow', 'purple', 'black', 'grey', 'brown']

SF2Path = "C:\\ProgramData\\soundfonts\\default.sf2"
MidiFilesPath = "C:\\Users\\admin\\Desktop\\newlife\\8 semester\\в последний путь\\midi"
DefaultMidiFile = "result.mid"

ChannelCnt = 16
A4 = 440

TonalitySequenceMajor = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'Bb', 'F']
TonalitySequenceMinor = ['A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'F', 'C', 'G', 'D']
TonalityCircle = dict({'major': [],
                       'minor': []})

# [numerator, denominator]
TimeSignature = [4, 4]
TicksPerBeat = 480
DefaultTempo = 40

BarsInTonality = 4
ProbabilityCurTonality = 0.4

BarsToGenerate = 10


#NotesDurations = [1, 0.5, 0.25, 0.125, 0.0625, 0.03125]
#NotesDurations = [1, 0.5, 0.25, 0.125, 0.0625]
NotesDurations = [1, 0.5, 0.25, 0.125,
                  1.5, 0.75, 0.375, 0.1875,
                  1.75, 0.875, 0.4375, 0.21875]

# не совсем constants, но уж как вышло
LuscherTestResult = []
LuscherTestCur = ['blue', 'green', 'red', 'yellow', 'purple', 'black', 'grey', 'brown']
LuscherTestDone = False


PATH1 = r"C:\Users\admin\Desktop\newlife\8 semester\в последний путь\midi\midi_songs"

PATH = r"C:\Users\admin\Desktop\newlife\8 semester\в последний путь\midi\1"

StatsUpdated = False
GenerationEnded = False

