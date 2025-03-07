from PyQt6.QtWidgets import QMainWindow

from forms.main_window import Ui_MainWindow
from src.controller import MapController


class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._controller = MapController()
        self._controller.set_view(self.map_canvas)
        self._controller.update()
