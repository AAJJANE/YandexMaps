import asyncio
from asyncio import Event

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QMainWindow
from qasync import asyncSlot

from forms.main_window import Ui_MainWindow
from src.controller import MapController


class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._controller = MapController()
        self._controller.set_view(self.map_canvas)
        self._controller.set_status_bar(self.statusbar)
        self.async_init()


    @asyncSlot()
    async def async_init(self):
        asyncio.create_task(self._controller.update())

    def keyPressEvent(self, event: QKeyEvent):
        self.handle_key_event(event.key())

    @asyncSlot()
    async def handle_key_event(self, key_id: int):
        match key_id:
            case Qt.Key.Key_PageUp:
                await self._controller.scale_up()
            case Qt.Key.Key_PageDown:
                await self._controller.scale_down()
            case Qt.Key.Key_Left:
                await self._controller.left()
            case Qt.Key.Key_Right:
                await self._controller.right()
            case Qt.Key.Key_Up:
                await self._controller.up()
            case Qt.Key.Key_Down:
                await self._controller.down()
