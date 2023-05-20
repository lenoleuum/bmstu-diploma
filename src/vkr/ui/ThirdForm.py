import tkinter as tk
from random import shuffle
from tkinter import font as tkFont

from .ForthForm import ForthForm

import sys
sys.path.append("..")

from constants.Constants import Constants
from utils.LuscherTestHandler import LuscherTestHandler


class ThirdForm:
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
        self.root.title('Тест Люшера 3')
        self.root['bg'] = Constants.WindowColor

        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()

        x = (ws / 2) - 500
        y = (hs / 2) - 200

        self.root.geometry('%dx%d+%d+%d' % (800, 200, x, y))

        lbl_font = tkFont.Font(family='Helvetica', size=8, weight=tkFont.NORMAL)
        label_test = tk.Label(self.root, text='Выберите наиболее приятный для Вас цвет', 
                              font=lbl_font, bg=Constants.WindowColor)
        label_test.place(x=20, y=20)

        self.color_setup()

    def color_setup(self):
        color_buttons = []
        offset = [30, 90]
        start = [20, 70]

        LuscherTestCurShuffled = LuscherTestHandler.LuscherTestCur
        shuffle(LuscherTestCurShuffled)

        for i in range(len(LuscherTestCurShuffled)):
            b = tk.Button(self.root, bg=Constants.ColorsDict.get(LuscherTestCurShuffled[i]),
                          width=10, command=lambda j=i: self.func_list.get(LuscherTestCurShuffled[j])())

            b.place(x=start[0] + offset[1] * i, y=start[1])

            color_buttons.append(b)

    def run(self):
        self.root.mainloop()

    def blue_clicked(self):
        LuscherTestHandler.LuscherTestResult.append(Constants.Colors[0])
        LuscherTestHandler.LuscherTestCur.remove(Constants.Colors[0])
        self.destroy()

    def green_clicked(self):
        LuscherTestHandler.LuscherTestResult.append(Constants.Colors[1])
        LuscherTestHandler.LuscherTestCur.remove(Constants.Colors[1])
        self.destroy()

    def red_clicked(self):
        LuscherTestHandler.LuscherTestResult.append(Constants.Colors[2])
        LuscherTestHandler.LuscherTestCur.remove(Constants.Colors[2])
        self.destroy()

    def yellow_clicked(self):
        LuscherTestHandler.LuscherTestResult.append(Constants.Colors[3])
        LuscherTestHandler.LuscherTestCur.remove(Constants.Colors[3])
        self.destroy()

    def purple_clicked(self):
        LuscherTestHandler.LuscherTestResult.append(Constants.Colors[4])
        LuscherTestHandler.LuscherTestCur.remove(Constants.Colors[4])
        self.destroy()

    def black_clicked(self):
        LuscherTestHandler.LuscherTestResult.append(Constants.Colors[5])
        LuscherTestHandler.LuscherTestCur.remove(Constants.Colors[5])
        self.destroy()

    def grey_clicked(self):
        LuscherTestHandler.LuscherTestResult.append(Constants.Colors[6])
        LuscherTestHandler.LuscherTestCur.remove(Constants.Colors[6])
        self.destroy()

    def brown_clicked(self):
        LuscherTestHandler.LuscherTestResult.append(Constants.Colors[7])
        LuscherTestHandler.LuscherTestCur.remove(Constants.Colors[7])
        self.destroy()

    def destroy(self):
        self.root.destroy()
        f = ForthForm()
        f.run()
