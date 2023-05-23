from pandas import *
import seaborn as sns
import matplotlib.pyplot as plt

def condition(x, comp):
    return x <= comp

def main():
    research_data = read_csv(r'C:\\Users\\admin\\Desktop\\newlife\\8 semester\\в последний путь\\VKR\vkr\\research\\result_v2.csv')
    cr_cnt = 5

    '''for i in range(cr_cnt):
        fig = plt.figure()
        sns.countplot(x='Критерий №' + str(i+1), data=research_data)
        plt.show()'''
    
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
    d, c = [], ['Критерии', '1', '2', '3', '4', '5']

    for i in range(cr_cnt):
        d.append(['Кр. ' + str(i + 1)] + cr_appearances[i][1])

    df = DataFrame(d, columns=c)
    
    df.plot(x='Критерии',
            kind='bar',
            stacked=False,
            title='Распределение оценок')

    plt.show()

    quantiles_cr_1 = research_data['Критерий №1'].quantile([0.25,0.5,0.75])
    quantiles_cr_2 = research_data['Критерий №2'].quantile([0.25,0.5,0.75])
    quantiles_cr_3 = research_data['Критерий №3'].quantile([0.25,0.5,0.75])
    quantiles_cr_4 = research_data['Критерий №4'].quantile([0.25,0.5,0.75])
    quantiles_cr_5 = research_data['Критерий №5'].quantile([0.25,0.5,0.75])

    quantiles = [quantiles_cr_1, quantiles_cr_2, quantiles_cr_3, quantiles_cr_4, quantiles_cr_5]
    cr_q_dicts = []

    print(quantiles)

    '''for i in range(cr_cnt):
        d = dict()
        q = quantiles[i]
        l = research_data['Критерий №'+str(i + 1)].tolist()


        if q[0.25] == q[0.5]:
            if q[0.5] == q[0.75]:
                d["Кр." + str(i) + " <= " + str(q[0.25]) + "(Q1, Q2, Q3)"] = sum(condition(x, q[0.5]) for x in l)
            else:
                d["Кр." + str(i) + " <= " + str(q[0.25]) + "(Q1, Q2)"] = sum(condition(x, q[0.5]) for x in l)
                d["Кр." + str(i) + " <= " + str(q[0.75]) + "(Q3)"] = sum(condition(x, q[0.75]) for x in l)
        else:
            d["Кр." + str(i) + " <= " + str(q[0.25]) + "(Q1)"] = sum(condition(x, q[0.25]) for x in l)

            if q[0.5] == q[0.75]:
                d["Кр." + str(i) + " <= " + str(q[0.5]) + "(Q2, Q3)"] = sum(condition(x, q[0.5]) for x in l)
            else:
                d["Кр." + str(i) + " <= " + str(q[0.5]) + "(Q2)"] = sum(condition(x, q[0.5]) for x in l)
                d["Кр." + str(i) + " <= " + str(q[0.75]) + "(Q3)"] = sum(condition(x, q[0.75]) for x in l)

        cr_q_dicts.append(d)'''


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

    bar_colors = ['tab:blue', 'tab:orange', 'tab:green',  'tab:purple']

    '''x, y = [], []
    bar_list = []

    for i in range(cr_cnt):
        x = list(cr_q_dicts[i].keys())
        y = list(cr_q_dicts[i].values())

        fig = plt.figure(figsize = (10, 5))
        
        bar_list.append(plt.bar(x, y))'''

    d, c = [], ['Критерии', 'Q1', 'Q2', 'Q3']

    for i in range(cr_cnt):
        y = list(cr_q_dicts[i].values())
        d.append(['Кр. ' + str(i + 1)] + y)

  
    df = DataFrame(d, columns=c)
    
    df.plot(x='Критерии',
            kind='bar',
            stacked=False,
            title='Распределение оценок по квартилям')

    plt.show()

    '''for j in range(len(bar_list)):
        bar_list[j].set_color(bar_colors[j])'''

        
    '''plt.xlabel("Квантили")
    plt.ylabel("Количество оценок")
    plt.title("Распределение оценок по квантилям (Критерий №" + str(i + 1) + ")")
    plt.show()'''

    '''for i in range(cr_cnt):
        x = list(cr_q_dicts[i].keys())
        y = list(cr_q_dicts[i].values())

        fig = plt.figure(figsize = (10, 5))
    
        bar_list = plt.bar(x, y)

        for j in range(len(bar_list)):
            bar_list[j].set_color(bar_colors[j])
        
        plt.xlabel("Квантили")
        plt.ylabel("Количество оценок")
        plt.title("Распределение оценок по квантилям (Критерий №" + str(i + 1) + ")")
        plt.show()'''

if __name__ == '__main__':
    main()