from pandas import *
import seaborn as sns
import matplotlib.pyplot as plt

def condition(x, comp):
    return x <= comp

def main():
    research_data = read_csv(r'C:\\Users\\admin\\Desktop\\newlife\\8 semester\\в последний путь\\VKR\vkr\\research\\result_v1.csv')
    cr_cnt = 5

    for i in range(cr_cnt):
        fig = plt.figure()
        sns.countplot(x='Критерий №' + str(i+1), data=research_data)
        plt.show()

    quantiles_cr_1 = research_data['Критерий №1'].quantile([0.25,0.5,0.75])
    quantiles_cr_2 = research_data['Критерий №2'].quantile([0.25,0.5,0.75])
    quantiles_cr_3 = research_data['Критерий №3'].quantile([0.25,0.5,0.75])
    quantiles_cr_4 = research_data['Критерий №4'].quantile([0.25,0.5,0.75])
    quantiles_cr_5 = research_data['Критерий №5'].quantile([0.25,0.5,0.75])

    quantiles = [quantiles_cr_1, quantiles_cr_2, quantiles_cr_3, quantiles_cr_4, quantiles_cr_5]
    cr_q_dicts = []

    print(quantiles)

    for i in range(cr_cnt):
        d = dict()
        q = quantiles[i]
        l = research_data['Критерий №'+str(i + 1)].tolist()


        if q[0.25] == q[0.5]:
            if q[0.5] == q[0.75]:
                d["<= " + str(q[0.25]) + "(Q1, Q2, Q3)"] = sum(condition(x, q[0.5]) for x in l)
            else:
                d["<= " + str(q[0.25]) + "(Q1, Q2)"] = sum(condition(x, q[0.5]) for x in l)
                d["<= " + str(q[0.75]) + "(Q3)"] = sum(condition(x, q[0.75]) for x in l)
        else:
            d["<= " + str(q[0.25]) + "(Q1)"] = sum(condition(x, q[0.25]) for x in l)

            if q[0.5] == q[0.75]:
                d["<= " + str(q[0.5]) + "(Q2, Q3)"] = sum(condition(x, q[0.5]) for x in l)
            else:
                d["<= " + str(q[0.5]) + "(Q2)"] = sum(condition(x, q[0.5]) for x in l)
                d["<= " + str(q[0.75]) + "(Q3)"] = sum(condition(x, q[0.75]) for x in l)

        cr_q_dicts.append(d)

    print(cr_q_dicts)

    bar_colors = ['tab:blue', 'tab:orange', 'tab:green',  'tab:purple']
    for i in range(cr_cnt):
        x = list(cr_q_dicts[i].keys())
        y = list(cr_q_dicts[i].values())

        fig = plt.figure(figsize = (10, 5))
    
        bar_list = plt.bar(x, y)

        for j in range(len(bar_list)):
            bar_list[j].set_color(bar_colors[j])
        
        plt.xlabel("Квантили")
        plt.ylabel("Количество оценок")
        plt.title("Распределение оценок по квантилям (Критерий №" + str(i + 1) + ")")
        plt.show()

if __name__ == '__main__':
    main()