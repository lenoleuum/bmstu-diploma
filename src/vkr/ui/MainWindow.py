import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo
import tkinter.filedialog as fd
import time
import sys

from .FirstForm import FirstForm

sys.path.append("..")

from constants.Constants import Constants
from utils.InputHandler import InputHandler
from utils.LuscherTestHandler import LuscherTestHandler
from stats.Parser import Parser
from stats.Classificator import Classificator
from generation.Generator import Generator
from utils.Converter import Converter

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.file = None
        self.dur = None

        self.parser = Parser(Constants.ColorsPath)
        self.classificator = Classificator()
        self.generator = Generator()
        self.converter = Converter()
        self.input_handler = InputHandler()
        self.luscher_test_handler = LuscherTestHandler()

        self.generated_fragment = None
        self.meta = None

    def setup(self):
        self.root.title("Аля диплом")
        self.root['bg'] = Constants.WindowColor

        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
                                                             
        x = (ws / 2) - 350
        y = (hs / 2) - 300

        self.root.geometry('%dx%d+%d+%d' % (800, 400, x, y))

        self.setup_input()
        self.setup_buttons()
        self.setup_menu()

    def setup_input(self):
        self.lbl_duration = tk.Label(self.root, text="Выберите длину генерируемого фрагмента в нотах: ", bg=Constants.WindowColor)
        self.lbl_duration.place(x=240, y=40)

        self.entry_duration = ttk.Spinbox(from_=100, to=1000, increment=10, width=10)
        self.entry_duration.place(x=540, y=42)


    def setup_buttons(self):
        canvas = tk.Canvas(self.root, width = 220, height = 300, bg = Constants.AdditionalColor)
        canvas.place(x = 0, y = 0)

        btn_luscher_test = tk.Button(canvas, text="Тест Люшера", width=20,
                                     command=lambda: self.start_LuscherTest())
        btn_luscher_test.place(x=35, y=20)

        btn_stats = tk.Button(canvas, text="Обновить статистику", width=20,
                                 command=lambda: self.update_stats())
        btn_stats.place(x=35, y=60)

        btn_generate = tk.Button(canvas, text="Генерация", width=20,
                                 command=lambda: self.start_generation())
        btn_generate.place(x=35, y=100)

        btn_play = tk.Button(canvas, text="Воспроизвести", width=20,
                             command=lambda: self.play_generated_fragment())
        btn_play.place(x=35, y=140)

        btn_download = tk.Button(canvas, text="Скачать", width=20,
                                 command=lambda: self.download_generated_fragment())
        btn_download.place(x=35, y=180)

        btn_exit = tk.Button(canvas, text="Выход", width=20,
                                 command=lambda: self.exit())
        btn_exit.place(x=35, y=220)


    def setup_menu(self):
        main_menu = tk.Menu()
        main_menu.add_cascade(label="Помощь", command=lambda: self.show_help())
        main_menu.add_cascade(label="О программе", command=lambda: self.show_info())

        self.root.config(menu=main_menu)

    def start_LuscherTest(self):
        if self.luscher_test_handler.LuscherTestDone:
            showerror(title="Ошибка", message="Вы уже прошли тест Люшера!")
        else:
            f = FirstForm()
            f.run()


    def start_generation(self):
        if self.luscher_test_handler.LuscherTestDone:
            self.meta = self.input_handler.handle(self.luscher_test_handler.LuscherTestResult)
            if self.entry_duration.get() == "":
                self.generated_fragment = self.generator.generate(self.meta)
            else:
                self.dur = self.entry_duration.get()
                self.generated_fragment = self.generator.generate(self.meta, length=int(self.dur))

            print("[meta] ", self.meta['color'], self.meta['lad'], self.meta['bpm'], self.meta['time_signature'])

            # todo: я начинаю генерацию с 4 октавы - оставляем?
            #generated_fragment = handle_generation(tonica + '4', tonality_gamma)

            # todo: process_input должен возвращать Tonality

            GenerationEnded = True
        else:
            showerror(title="Ошибка", message="Сначала пройдите тест Люшера!")

    def play_generated_fragment(self):
        if self.file is not None:
            self.converter.play(self.file)
        else:
            showerror(title="Ошибка", message="Вы еще не сгенерировали музыкальный фрагмент!")

    def download_generated_fragment(self):
        if self.generated_fragment is not None:
            self.file = self.converter.convert(self.generated_fragment, self.meta)
            print(self.file)
        else:
            showerror(title="Ошибка", message="Вы еще не сгенерировали музыкальный фрагмент!")
            return

        '''directory = fd.asksaveasfilename(title="Открыть папку", initialdir="/")

        if directory:
            if ".mid" in directory.lower() or ".midi" in directory.lower():
                self.file.download_midi_file(directory)
            else:
                self.file.download_midi_file(directory + ".mid")'''

    @staticmethod
    def update_stats():
        if not True:
            c = Classificator()
            c.classify()

            p = Parser(Constants.ColorsPath)
            p.parse()
        else:
            showerror(title="Ошибка", message="Вы уже обновляли статистику!")

    @staticmethod
    def show_info():
        showinfo(title="О Программе", message="ВКР на тему\n'Метод генерации музыкального фрагмента,\n"
                                              "соответсвующего эмоциональному состоянию человека,\nс использованием "
                                              "марковских моделей'\n "
                                              "Автор: Фролова Лена ИУ7-81Б")

    @staticmethod
    def show_help():
        showinfo(title="Помощь", message="Мне бы кто помог...")

    def run(self):
        self.root.mainloop()

    def exit(self):
        self.root.destroy()
