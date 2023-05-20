import os

class Constants:
    # ui
    WindowColor = 'white'
    AdditionalColor = '#87CEFA'
    AdditionalColorInfo ='#ADD8E6'

    #WorkDir = r"C:\Users\admin\Desktop\newlife\8 semester\в последний путь\VKR\samples"
    WorkDir = os.getcwd()

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

    ColorsPath = os.path.split(WorkDir)[0] + "\\training data\\colors"
    TracksPath = os.path.split(WorkDir)[0] + "\\training data\\tracks"

    Lads = ['major', 'minor']

    '''TempoDict = dict({'red': dict({'presto': [150, 200], 'vivace': [132, 150]}),
                      'yellow': dict({'moderato': [86, 109], 'allegro': [109, 132]}),
                      'green': dict({'moderato': [86, 109], 'allegro': [109, 132]}),
                      'blue': dict({'lento': [30, 50], 'adagio': [50, 73], 'andante': [73, 86]})})'''
    
    TempoDict = dict({'red minor': dict({'allegro': [109, 132]}),
                      'red major': dict({'allegro': [109, 132], 'vivace': [132, 150]}),
                      'yellow minor': dict({'andante': [73, 86], 'moderato': [86, 109]}),
                      'yellow major': dict({'moderato': [86, 109], 'allegro': [109, 132]}),
                      'green minor': dict({'andante': [73, 86], 'moderato': [86, 109]}),
                      'green major': dict({'moderato': [86, 109], 'allegro': [109, 132]}),
                      'blue minor': dict({'lento': [30, 50], 'adagio': [50, 73]}),
                      'blue major': dict({'adagio': [50, 73], 'andante': [73, 86]})})
    
    TrainingDataToEmotionDict = dict({
                    'red minor': 'Негативные эмоции (тревожность/стресс/грусть/огорчение)',
                    'red major': 'Возбуждение, энергичность',
                    'yellow minor': 'Негативные эмоции (тревожность/стресс/грусть/огорчение)',
                    'yellow major': 'Активность, веселость',
                    'green minor': 'Негативные эмоции (тревожность/стресс/грусть/огорчение)',
                    'green major': 'Уверенность, настойчивость',
                    'blue minor': 'Негативные эмоции (тревожность/стресс/грусть/огорчение)',
                    'blue major': 'Спокойствие, удовлетворенность'})
    
    #TimeSignatureList = list(['2/4', '3/4', '4/4', '3/8', '6/8'])
    TimeSignatureList = list(['2/4', '3/4', '4/4', '6/8'])
