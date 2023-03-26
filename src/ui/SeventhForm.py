import tkinter as tk
from random import shuffle

import sys
sys.path.append("..")

import constants.Constants as consts #import WindowColor, LuscherTestCur, ColorsDict, LuscherTestResult, Colors


class SeventhForm:
    def __init__(self):
        self.func_list = dict({'blue': lambda: self.blue_clicked(),
                               'green': lambda: self.green_clicked(),
                               'red': lambda: self.red_clicked(),
                               'yellow': lambda: self.yellow_clicked(),
                               'purple': lambda: self.purple_clicked(),
                               'black': lambda: self.black_clicked(),
                               'grey': lambda: self.grey_clicked(),
                               'brown': lambda: self.brown_clicked()})
        self.root = tk.Tk()
        self.setup()

    def setup(self):
        self.root.title('Тест Люшера 7')
        self.root['bg'] = consts.WindowColor

        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()

        x = (ws / 2) - 500
        y = (hs / 2) - 200

        self.root.geometry('%dx%d+%d+%d' % (800, 200, x, y))

        label_test = tk.Label(self.root, text='Выберите наиболее приятный для Вас цвет', bg=consts.WindowColor)
        label_test.place(x=20, y=10)

        self.color_setup()

    def color_setup(self):
        color_buttons = []
        offset = [30, 90]
        start = [20, 70]

        LuscherTestCurShuffled = consts.LuscherTestCur
        shuffle(LuscherTestCurShuffled)

        for i in range(len(LuscherTestCurShuffled)):
            b = tk.Button(self.root, bg=consts.ColorsDict.get(LuscherTestCurShuffled[i]),
                          width=10, command=lambda j=i:  self.func_list.get(LuscherTestCurShuffled[j])())

            b.place(x=start[0] + offset[1] * i, y=start[1])

            color_buttons.append(b)

    def run(self):
        self.root.mainloop()

    def blue_clicked(self):
        consts.LuscherTestResult.append(consts.Colors[0])
        consts.LuscherTestCur.remove(consts.Colors[0])

        consts.LuscherTestResult.append(consts.LuscherTestCur[0])

        self.destroy()

    def green_clicked(self):
        consts.LuscherTestResult.append(consts.Colors[1])
        consts.LuscherTestCur.remove(consts.Colors[1])

        consts.LuscherTestResult.append(consts.LuscherTestCur[0])

        self.destroy()

    def red_clicked(self):
        consts.LuscherTestResult.append(consts.Colors[2])
        consts.LuscherTestCur.remove(consts.Colors[2])

        consts.LuscherTestResult.append(consts.LuscherTestCur[0])

        self.destroy()

    def yellow_clicked(self):
        consts.LuscherTestResult.append(consts.Colors[3])
        consts.LuscherTestCur.remove(consts.Colors[3])

        consts.LuscherTestResult.append(consts.LuscherTestCur[0])

        self.destroy()

    def purple_clicked(self):
        consts.LuscherTestResult.append(consts.Colors[4])
        consts.LuscherTestCur.remove(consts.Colors[4])

        consts.LuscherTestResult.append(consts.LuscherTestCur[0])

        self.destroy()

    def black_clicked(self):
        consts.LuscherTestResult.append(consts.Colors[5])
        consts.LuscherTestCur.remove(consts.Colors[5])

        consts.LuscherTestResult.append(consts.LuscherTestCur[0])

        self.destroy()

    def grey_clicked(self):
        consts.LuscherTestResult.append(consts.Colors[6])
        consts.LuscherTestCur.remove(consts.Colors[6])

        consts.LuscherTestResult.append(consts.LuscherTestCur[0])

        self.destroy()

    def brown_clicked(self):
        consts.LuscherTestResult.append(consts.Colors[7])
        consts.LuscherTestCur.remove(consts.Colors[7])

        consts.LuscherTestResult.append(consts.LuscherTestCur[0])

        self.destroy()

    def destroy(self):
        consts.LuscherTestDone = True
        self.root.destroy()
