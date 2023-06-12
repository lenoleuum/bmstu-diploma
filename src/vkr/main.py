from ui.MainWindow import MainWindow
import os
import shutil


def main():
    root = MainWindow()
    root.setup()
    root.run()
    

if __name__ == '__main__':
    shutil.rmtree("./ui/tmp") 
    os.mkdir("./ui/tmp", mode=0o777)
    main()
    