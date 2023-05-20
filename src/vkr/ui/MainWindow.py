import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo, askyesnocancel
import tkinter.filedialog as fd
import time
import sys
from tkinter import font as tkFont
import os
import shutil
from PIL import ImageTk

from .FirstForm import FirstForm

sys.path.append("..")

from constants.Constants import Constants
from utils.InputHandler import InputHandler
from utils.LuscherTestHandler import LuscherTestHandler
from analyze.Parser import Parser
from analyze.Classificator import Classificator
from generation.Generator import Generator
from utils.Converter import Converter
from utils.Transformer import Transformer

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
        self.transformer = Transformer()

        self.generated_fragment = None
        self.meta = None

        self.fragment_format = "midi"

        self.playback = None

    def setup(self):
        self.root.title("ВКР")
        self.root['bg'] = Constants.WindowColor

        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
                                                             
        x = (ws / 2) - 350
        y = (hs / 2) - 300

        #self.root.geometry('%dx%d+%d+%d' % (800, 400, x, y))

        width= self.root.winfo_screenwidth()               
        height= self.root.winfo_screenheight()

        self.root.geometry("%dx%d" % (width, height))

        self.setup_input()
        self.setup_buttons()
        self.setup_menu()
        self.setup_fragment_info()

    def select_format(self, format_var): 
        if format_var.get() == 1:
            self.fragment_format = "midi"
        else:
            self.fragment_format = "mp3"

    def setup_input(self):
        rb_font = tkFont.Font(family='Helvetica', size=12, weight=tkFont.NORMAL)

        self.lbl_duration = tk.Label(self.root, text="Длина фрагмента в звуковых объектах: ", 
                                     font=rb_font, bg=Constants.WindowColor)
        self.lbl_duration.place(x=460, y=300)

        self.entry_duration = ttk.Spinbox(from_=100, to=1000, increment=10, width=10)
        self.entry_duration.place(x=770, y=300)

        format = tk.IntVar() 
        format_lbl = tk.Label(text = "Формат музыкального фрагмента для скачивания", font=rb_font, bg=Constants.WindowColor) 
        format_lbl.place(x=460, y=400)

        midi_rb = tk.Radiobutton(self.root, text="midi", variable=format, value=1, 
                        font=rb_font, bg=Constants.WindowColor,
                        command=lambda: self.select_format(format)) 
        midi_rb.place(x=460, y=430)
        
        mp3_rb = tk.Radiobutton(self.root, text="mp3", variable=format, value=2, 
                        font=rb_font, bg=Constants.WindowColor,
                        command=lambda: self.select_format(format)) 
        mp3_rb.place(x=460, y=450)
        
        if self.fragment_format == "midi":
            format.set(1)
        else:
            format.set(2)

        self.normalize = tk.IntVar()
  
        normalize_cb = tk.Checkbutton(text="Нормализация фрагмента", variable=self.normalize,
                                       font=rb_font, bg=Constants.WindowColor)
        normalize_cb.place(x=460, y=490)


    def setup_buttons(self):
        canvas = tk.Canvas(self.root, width = 430, height = self.root.winfo_screenheight(), bg = Constants.AdditionalColor)
        canvas.place(x = 0, y = 0)

        button_font = tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)

        btn_luscher_test = tk.Button(canvas, text="\nТест Люшера\n", width=30, font=button_font,
                                     command=lambda: self.start_LuscherTest())
        btn_luscher_test.place(x=50, y=50)

        '''btn_stats = tk.Button(canvas, text="Обновить статистику", width=20,
                                 command=lambda: self.update_stats())
        btn_stats.place(x=35, y=60)'''

        btn_generate = tk.Button(canvas, text="\nСгенерировать фрагмент\n", width=30, font=button_font,
                                 command=lambda: self.start_generation())
        btn_generate.place(x=50, y=150)

        btn_download = tk.Button(canvas, text="\nСкачать фрагмент\n", width=30, font=button_font,
                                 command=lambda: self.download_generated_fragment())
        btn_download.place(x=50, y=250)

        '''self.image_play = tk.PhotoImage(file="C:\\Users\\admin\\Desktop\\newlife\\8 semester\\в последний путь\\VKR\\vkr\\ui\\play.png")
        self.image_play = self.image_play.subsample(19, 19)
        self.btn_play = tk.Button(self.root, image=self.image_play, width=50, height=50,
                             command=lambda: self.play_generated_fragment())
        self.btn_play.place(x=120, y=350)'''

        self.btn_play = tk.Button(canvas, text="\nВоспроизвести\n", font=button_font, width=30,
                             command=lambda: self.play_generated_fragment())
        self.btn_play.place(x=50, y=350)

        '''self.image_pause = tk.PhotoImage(file="C:\\Users\\admin\\Desktop\\newlife\\8 semester\\в последний путь\\VKR\\vkr\\ui\\pause.png")
        self.image_pause = self.image_pause.subsample(18, 18)
        self.btn_pause = tk.Button(self.root, image=self.image_pause, width=50, height=50,
                             command=lambda: self.stop_playing())
        self.btn_pause.place(x=220, y=350)'''

        btn_exit = tk.Button(canvas, text="\nВыход\n", width=30, font=button_font,
                                 command=lambda: self.exit())
        btn_exit.place(x=50, y=450)

    def setup_fragment_info(self):
        canvas = tk.Canvas(self.root, width = self.root.winfo_screenwidth() - 430, height = 150, bg = Constants.AdditionalColorInfo)
        canvas.place(x = 432, y = 0)

        header_font = tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)
        info_font = tkFont.Font(family='Helvetica', size=10, weight=tkFont.NORMAL)

        fragment_info_lbl = tk.Label(self.root, text="Информация о сгенерированном фрагменте", 
                                     font=header_font, bg=Constants.AdditionalColorInfo)
        fragment_info_lbl.place(x=630, y=20)

        training_data_lbl = tk.Label(self.root, text="Обучающий набор данных: ", 
                                          font=info_font, bg=Constants.AdditionalColorInfo)
        training_data_lbl.place(x=460, y=60)

        self.training_data_lbl_value = tk.Label(self.root, text="", 
                                          font=info_font, bg=Constants.AdditionalColorInfo)
        self.training_data_lbl_value.place(x=650, y=60)

        emotion_lbl = tk.Label(self.root, text="Эмоциональная окраска: ", 
                                          font=info_font, bg=Constants.AdditionalColorInfo)
        emotion_lbl.place(x=460, y=100)

        self.emotion_lbl_value = tk.Label(self.root, text="", 
                                          font=info_font, bg=Constants.AdditionalColorInfo)
        self.emotion_lbl_value.place(x=650, y=100)


    '''def setup_demo(self):
        enabled = IntVar()
  
        enabled_checkbutton = ttk.Checkbutton(text="Включить", variable=enabled)
        enabled_checkbutton.pack(padx=6, pady=6, anchor=NW)
        
        enabled_label = ttk.Label(textvariable=enabled)
        enabled_label.pack(padx=6, pady=6, anchor=NW)'''

    def setup_menu(self):
        main_menu = tk.Menu()
        main_menu.add_cascade(label="О программе", command=lambda: self.show_info())
        main_menu.add_cascade(label="Помощь", command=lambda: self.show_help())

        self.root.config(menu=main_menu)

    def start_LuscherTest(self):
        answer = False
        if LuscherTestHandler.LuscherTestDone:
            answer = askyesnocancel(title='Подтверждение',
                                    message='Вы уверены, что хотите пройти тест Люшера заново?')
            
            if answer:
                self.luscher_test_handler.clear_results()
                LuscherTestHandler.LuscherTestDone = False

        if not LuscherTestHandler.LuscherTestDone:
            f = FirstForm()
            f.run()


    def start_generation(self):
        if LuscherTestHandler.LuscherTestDone:
            self.meta = self.input_handler.handle(self.luscher_test_handler.LuscherTestResult)
            if self.entry_duration.get() == "":
                self.generated_fragment = self.generator.generate(self.meta)
            else:
                self.dur = self.entry_duration.get()
                self.generated_fragment = self.generator.generate(self.meta, length=int(self.dur))

            training_data = self.meta['color'] + " " + self.meta['lad']
            self.training_data_lbl_value['text'] = training_data
            self.emotion_lbl_value['text'] = Constants.TrainingDataToEmotionDict[training_data]

            print("[meta] ", self.meta['color'], self.meta['lad'], self.meta['bpm'], self.luscher_test_handler.LuscherTestResult[7])

            self.file = self.converter.convert(self.generated_fragment, self.meta)
        else:
            showerror(title="Ошибка", message="Сначала пройдите тест Люшера!")


    def play_generated_fragment(self):
        if self.file is not None:
            #self.converter.play_midi(self.file)

            tmp_filename = "tmp.mp3"
            self.transformer.midi_to_mp3(self.file, tmp_filename)

            self.playback = self.transformer.play_mp3(tmp_filename)

            os.remove(tmp_filename)

        else:
            showerror(title="Ошибка", message="Вы еще не сгенерировали музыкальный фрагмент!")


    def stop_playing(self):
        if self.playback:
            self.transformer.stop_mp3(self.playback)
        else:
            showerror(title="Ошибка", message="Вы еще не сгенерировали музыкальный фрагмент!")


    def download_generated_fragment(self):
        if self.file is not None:
            if self.fragment_format == "midi":
                midi_filename = fd.asksaveasfile(initialdir=os.getcwd(), mode='w', filetypes=[("Midi Music file", "*.mid")], defaultextension=".mid")
                shutil.copy2(self.file, midi_filename.name)

            elif self.fragment_format == "mp3":
                if self.normalize == 1:
                    tmp_filename = "tmp.mp3"
                    mp3_filename = fd.asksaveasfile(initialdir=os.getcwd(), mode='w', filetypes=[("Mp3 Music file", "*.mp3")], defaultextension=".mp3")
                    self.transformer.midi_to_mp3(self.file, tmp_filename)
                    self.transformer.normalize(tmp_filename, mp3_filename.name)
                    os.remove(tmp_filename)
                else:
                    mp3_filename = fd.asksaveasfile(initialdir=os.getcwd(), mode='w', filetypes=[("Mp3 Music file", "*.mp3")], defaultextension=".mp3")
                    self.transformer.midi_to_mp3(self.file, mp3_filename.name)
        else:
            showerror(title="Ошибка", message="Вы еще не сгенерировали музыкальный фрагмент!")
            return

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
