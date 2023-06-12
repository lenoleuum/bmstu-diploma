from pandas import *
import seaborn as sns
import matplotlib.pyplot as plt
import math

def condition(x, comp):
    return x <= comp

def mean(xs): 
    return sum(xs) / len(xs) 

def variance(xs):
    mu = mean(xs)
    n = len(xs)
    n = n-1 if n in range(1, 30) else n  
    square_deviation = lambda x : (x - mu) ** 2
    return sum( map(square_deviation, xs) ) / n
    
def standard_deviation(xs):
     return math.sqrt( variance(xs) )

def main():
    research_data = read_csv(r'C:\\Users\\admin\\Desktop\\newlife\\8 semester\\в последний путь\\VKR\vkr\\research\\all_data.csv')
    cr_cnt = 5
    
    cr_1_appearances = [research_data['Критерий №1'].value_counts().sort_index().index.tolist(), 
                        research_data['Критерий №1'].value_counts().sort_index().to_frame()['Критерий №1'].to_list()]
    cr_2_appearances = [research_data['Критерий №2'].value_counts().sort_index().index.tolist(), 
                        research_data['Критерий №2'].value_counts().sort_index().to_frame()['Критерий №2'].to_list()]
    cr_3_appearances = [research_data['Критерий №3'].value_counts().sort_index().index.tolist(), 
                        research_data['Критерий №3'].value_counts().sort_index().to_frame()['Критерий №3'].to_list()]
    cr_4_appearances = [research_data['Критерий №4'].value_counts().sort_index().index.tolist(), 
                        research_data['Критерий №4'].value_counts().sort_index().to_frame()['Критерий №4'].to_list()]
    cr_5_appearances = [research_data['Критерий №5'].value_counts().sort_index().index.tolist(), 
                        research_data['Критерий №5'].value_counts().sort_index().to_frame()['Критерий №5'].to_list()]

    cr_appearances = [cr_1_appearances, cr_2_appearances, cr_3_appearances, cr_4_appearances, cr_5_appearances]
    d, c = [], ['Критерии', 'Оценка 1', 'Оценка 2', 'Оценка 3', 'Оценка 4', 'Оценка 5']
    '''name = ['Соответствие сгенерированного фрагмента заданной эмоциональной окраске',
            'Реалистичность звучания фортепиано',
            'Приятность/благозвучность мелодии для восприятия',
            'Цельность фрагмента',
            'Реалистичность отдельных фраз фрагмента']'''

    for i in range(cr_cnt):
        d.append(['Кр. ' + str(i + 1)] + cr_appearances[i][1])
        #d.append([name[i]] + cr_appearances[i][1])

    df = DataFrame(d, columns=c)
    
    dplot = df.plot(x='Критерии',
            kind='bar',
            stacked=False,
            title='Распределение оценок',
            color=['red', 'orange', 'palegreen', 'limegreen', 'forestgreen'],
            legend=True, width=0.9)
    
    dplot.set(ylabel='Количество оценок (шт.)')

    plt.show()

    quantiles_cr_1 = research_data['Критерий №1'].quantile([0.25,0.5,0.75])
    quantiles_cr_2 = research_data['Критерий №2'].quantile([0.25,0.5,0.75])
    quantiles_cr_3 = research_data['Критерий №3'].quantile([0.25,0.5,0.75])
    quantiles_cr_4 = research_data['Критерий №4'].quantile([0.25,0.5,0.75])
    quantiles_cr_5 = research_data['Критерий №5'].quantile([0.25,0.5,0.75])

    quantiles = [quantiles_cr_1, quantiles_cr_2, quantiles_cr_3, quantiles_cr_4, quantiles_cr_5]
    
    coeff_variation = [variance(research_data['Критерий №1']) / mean(research_data['Критерий №1']),
                       variance(research_data['Критерий №2']) / mean(research_data['Критерий №2']),
                       variance(research_data['Критерий №3']) / mean(research_data['Критерий №3']),
                       variance(research_data['Критерий №4']) / mean(research_data['Критерий №4']),
                       variance(research_data['Критерий №5']) / mean(research_data['Критерий №5'])]
    
    print(coeff_variation)

    cr_q_dicts = []

    for i in range(cr_cnt):
        d = dict()
        q = quantiles[i]
        l = research_data['Критерий №'+str(i + 1)].tolist()


        if q[0.25] == q[0.5]:
            if q[0.5] == q[0.75]:
                d["<= " + str(q[0.25]) + "(Q1)"] = sum(condition(x, q[0.5]) for x in l)
                d["<= " + str(q[0.25]) + "(Q2)"] = sum(condition(x, q[0.5]) for x in l)
                d["<= " + str(q[0.25]) + "(Q3)"] = sum(condition(x, q[0.5]) for x in l)
            else:
                d["<= " + str(q[0.25]) + "(Q1)"] = sum(condition(x, q[0.5]) for x in l)
                d["<= " + str(q[0.25]) + "(Q2)"] = sum(condition(x, q[0.5]) for x in l)
                d["<= " + str(q[0.75]) + "(Q3)"] = sum(condition(x, q[0.75]) for x in l)
        else:
            d["<= " + str(q[0.25]) + "(Q1)"] = sum(condition(x, q[0.25]) for x in l)

            if q[0.5] == q[0.75]:
                d["<= " + str(q[0.5]) + "(Q2)"] = sum(condition(x, q[0.5]) for x in l)
                d["<= " + str(q[0.5]) + "(Q3)"] = sum(condition(x, q[0.5]) for x in l)
            else:
                d["<= " + str(q[0.5]) + "(Q2)"] = sum(condition(x, q[0.5]) for x in l)
                d["<= " + str(q[0.75]) + "(Q3)"] = sum(condition(x, q[0.75]) for x in l)

        cr_q_dicts.append(d)

    print(cr_q_dicts)

    d, c = [], ['Критерии', 'Q1', 'Q2', 'Q3']

    for i in range(cr_cnt):
        y = list(cr_q_dicts[i].values())
        d.append(['Кр. ' + str(i + 1)] + y)

  
    df = DataFrame(d, columns=c)
    
    dplot = df.plot(x='Критерии',
            kind='bar',
            stacked=False,
            title='Распределение оценок по квартилям',
            color=['red', 'orange', 'forestgreen'])
    
    dplot.set(ylabel="Количество оценок (шт.)") 

    plt.show()

if __name__ == '__main__':
    main()