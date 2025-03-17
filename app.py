import asyncio

import getostheme
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QMainWindow
from qasync import asyncSlot

from forms.main_window import Ui_MainWindow
from src.static import MapController
from src.toponym import ToponymController


class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._static_controller = MapController()
        self._static_controller.set_view(self.map_canvas)
        self._static_controller.set_status_bar(self.statusbar)

        self._toponym_controller = ToponymController()
        self._toponym_controller.set_output_view(self.textFullAddress)
        self._toponym_controller.set_static_controller(self._static_controller)

        self.checkDarkTheme.stateChanged.connect(self.changeTheme)
        self.btnAddress.clicked.connect(self.handle_toponym_search)
        self.inputAddress.returnPressed.connect(self.handle_toponym_search)
        self.btnClear.clicked.connect(self.handle_toponym_clear)
        self.isPostalCode.stateChanged.connect(self.show_postal_code)
        self.async_init()
        if getostheme.isDarkMode():
            self.checkDarkTheme.setChecked(True)

    @asyncSlot()
    async def changeTheme(self):
        await self._static_controller.set_theme(self.checkDarkTheme.isChecked())

    @asyncSlot()
    async def async_init(self):
        asyncio.create_task(self._static_controller.update())

    def keyPressEvent(self, event: QKeyEvent):
        self.handle_key_event(event.key())

    @asyncSlot()
    async def handle_key_event(self, key_id: int):
        print(key_id)
        match key_id:
            case Qt.Key.Key_PageUp:
                await self._static_controller.scale_up()
            case Qt.Key.Key_PageDown:
                await self._static_controller.scale_down()
            case Qt.Key.Key_Left | Qt.Key.Key_A:
                await self._static_controller.left()
            case Qt.Key.Key_Right | Qt.Key.Key_D:
                await self._static_controller.right()
            case Qt.Key.Key_Up | Qt.Key.Key_W:
                await self._static_controller.up()
            case Qt.Key.Key_Down | Qt.Key.Key_S:
                await self._static_controller.down()

    @asyncSlot()
    async def handle_toponym_search(self):
        await self._toponym_controller.update_toponym(self.inputAddress.text())
        self.show_postal_code()

    @asyncSlot()
    async def handle_toponym_clear(self):
        await self._toponym_controller.update_toponym('')

    def show_postal_code(self):
        self._toponym_controller.update_postal_code(self.isPostalCode.isChecked())
