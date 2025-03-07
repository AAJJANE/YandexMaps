from asyncio import Event

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
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

    def keyPressEvent(self, event: QKeyEvent):
        match event.key():
            case Qt.Key.Key_PageUp:
                self._controller.scale_up()
            case Qt.Key.Key_PageDown:
                self._controller.scale_down()
            case Qt.Key.Key_Left:
                self._controller.left()
            case Qt.Key.Key_Right:
                self._controller.right()
            case Qt.Key.Key_Up:
                self._controller.up()
            case Qt.Key.Key_Down:
                self._controller.down()
