import asyncio

import getostheme
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QStyleFactory
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
        self.checkDarkTheme.stateChanged.connect(self.changeTheme)
        self.async_init()
        if getostheme.isDarkMode():
            self.checkDarkTheme.setChecked(True)

    @asyncSlot()
    async def changeTheme(self):
        await self._controller.set_theme(self.checkDarkTheme.isChecked())

    @asyncSlot()
    async def async_init(self):
        asyncio.create_task(self._controller.update())

    def keyPressEvent(self, event: QKeyEvent):
        self.handle_key_event(event.key())

    @asyncSlot()
    async def handle_key_event(self, key_id: int):
        print(key_id)
        match key_id:
            case Qt.Key.Key_PageUp:
                await self._controller.scale_up()
            case Qt.Key.Key_PageDown:
                await self._controller.scale_down()
            case Qt.Key.Key_Left | Qt.Key.Key_A:
                await self._controller.left()
            case Qt.Key.Key_Right | Qt.Key.Key_D:
                await self._controller.right()
            case Qt.Key.Key_Up | Qt.Key.Key_W:
                await self._controller.up()
            case Qt.Key.Key_Down | Qt.Key.Key_S:
                await self._controller.down()
