import tkinter as tk

from .SecondForm import SecondForm

import sys
sys.path.append("..")

from constants.Constants import WindowColor, ColorsNum, ColorsDict, Colors, LuscherTestResult, LuscherTestCur


class FirstForm:
    def __init__(self):
        self.func_list = [lambda: self.blue_clicked(),
                     lambda: self.green_clicked(),
                     lambda: self.red_clicked(),
                     lambda: self.yellow_clicked(),
                     lambda: self.purple_clicked(),
                     lambda: self.black_clicked(),
                     lambda: self.grey_clicked(),
                     lambda: self.brown_clicked()]
        self.root = tk.Tk()
        self.setup()

    def setup(self):
        self.root.title('Тест Люшера 1')
        self.root['bg'] = WindowColor

        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()

        x = (ws / 2) - 500
        y = (hs / 2) - 200

        self.root.geometry('%dx%d+%d+%d' % (800, 200, x, y))

        label_test = tk.Label(self.root, text='Выберите наиболее приятный для Вас цвет', bg=WindowColor)
        label_test.place(x=20, y=10)

        self.color_setup()

    def color_setup(self):
        color_buttons = []
        offset = [30, 90]
        start = [20, 70]

        for i in range(ColorsNum):
            b = tk.Button(self.root, bg=ColorsDict.get(Colors[i]),
                          width=10, command=lambda j=i: self.func_list[j]())

            b.place(x=start[0] + offset[1] * i, y=start[1])

            color_buttons.append(b)

    def run(self):
        self.root.mainloop()

    def blue_clicked(self):
        LuscherTestResult.append(Colors[0])
        LuscherTestCur.remove(Colors[0])
        self.destroy()

    def green_clicked(self):
        LuscherTestResult.append(Colors[1])
        LuscherTestCur.remove(Colors[1])
        self.destroy()

    def red_clicked(self):
        LuscherTestResult.append(Colors[2])
        LuscherTestCur.remove(Colors[2])
        self.destroy()

    def yellow_clicked(self):
        LuscherTestResult.append(Colors[3])
        LuscherTestCur.remove(Colors[3])
        self.destroy()

    def purple_clicked(self):
        LuscherTestResult.append(Colors[4])
        LuscherTestCur.remove(Colors[4])
        self.destroy()

    def black_clicked(self):
        LuscherTestResult.append(Colors[5])
        LuscherTestCur.remove(Colors[5])
        self.destroy()

    def grey_clicked(self):
        LuscherTestResult.append(Colors[6])
        LuscherTestCur.remove(Colors[6])
        self.destroy()

    def brown_clicked(self):
        LuscherTestResult.append(Colors[7])
        LuscherTestCur.remove(Colors[7])
        self.destroy()

    def destroy(self):
        self.root.destroy()
        f = SecondForm()
        f.run()
