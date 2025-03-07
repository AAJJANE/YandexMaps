import sys

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow

from app import App


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    app.exec()
