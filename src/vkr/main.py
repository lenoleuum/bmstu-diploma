from ui.MainWindow import MainWindow
import os
import shutil


def main():
    os.mkdir("/ui/tmp", mode=0o777)
    root = MainWindow()
    root.setup()
    root.run()
    shutil.rmtree("/ui/tmp") 

if __name__ == '__main__':
    main()