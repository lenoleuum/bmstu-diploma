import tkinter as tk
from tkinter import ttk
from LuscherTest.FirstForm import FirstForm
import Constants as const
from tkinter.messagebox import showerror, showwarning, showinfo
import tkinter.filedialog as fd

from MyMidiFile import MidiFile
from ProcessInput import process_input, translate_note, translate_lad
from GenerateFragment import handle_generation, generate_music_fragment
from Tonality import  Tonality


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.file = None

    def setup(self):
        self.root.title("Аля диплом")
        self.root['bg'] = const.WindowColor

        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()

        x = (ws / 2) - 500
        y = (hs / 2) - 300

        self.root.geometry('%dx%d+%d+%d' % (1000, 500, x, y))

        btn_luscher_test = tk.Button(self.root, text="Тест Люшера", width=20,
                                     command=lambda: self.start_LuscherTest())
        btn_luscher_test.place(x=10, y=10)

        # todo: что делаем с длительностью?
        # l_duration = tk.Label(self.root, text="Выберите длительность генерируемого фрагмента ")

        btn_generate = tk.Button(self.root, text="Начать генерацию", width=20,
                                 command=lambda: self.start_generation())
        btn_generate.place(x=10, y=40)

        btn_play = tk.Button(self.root, text="Воспроизвести", width=20,
                             command=lambda: self.play_generated_fragment())
        btn_play.place(x=10, y=100)

        '''
        file_name_entry = ttk.Entry(width=40)
        file_name_entry.place(x=10,y=150)
        '''

        btn_download = tk.Button(self.root, text="Скачать", width=20,
                                 command=lambda: self.download_generated_fragment())
        btn_download.place(x=10, y=200)

        self.setup_menu()

    def setup_menu(self):
        main_menu = tk.Menu()
        main_menu.add_cascade(label="Помощь", command=lambda: self.show_help())
        main_menu.add_cascade(label="О программе", command=lambda: self.show_info())

        self.root.config(menu=main_menu)

    # todo: перемешвать цвета при выборе + в одну линию
    @staticmethod
    def start_LuscherTest():
        if const.LuscherTestDone:
            showerror(title="Ошибка", message="Вы уже прошли тест Люшера!")
        else:
            f = FirstForm()
            f.run()

    def start_generation(self):
        if const.LuscherTestDone:
            lad, tonica, tonality_gamma = process_input(const.LuscherTestResult)
            showinfo(title='Результат', message='Тональность музыкального фрагмента:\n'
                                                + translate_note(tonica) + ' ' + translate_lad(lad))

            # todo: я начинаю генерацию с 4 октавы - оставляем?
            #generated_fragment = handle_generation(tonica + '4', tonality_gamma)

            # todo: process_input должен возвращать Tonality
            generated_fragment = generate_music_fragment(Tonality(lad, tonica))

            self.file = MidiFile(const.DefaultMidiFile)
            self.file.add_track(generated_fragment)
            self.file.save_midi_file()
        else:
            showerror(title="Ошибка", message="Сначала пройдите тест Люшера!")

    def play_generated_fragment(self):
        self.file.play()

    def download_generated_fragment(self):
        directory = fd.askdirectory(title="Открыть папку", initialdir="/")

        if directory:
            self.file.download_midi_file(directory + "/" + const.DefaultMidiFile)

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
