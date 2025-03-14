import asyncio
from asyncio import Task
from functools import wraps
from time import sleep
from typing import Callable

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QStatusBar

from .api import MapApi
from .model import MapModel, InitialMapModel


class MapController:
    _api = MapApi()
    SCALE_COEFFICIENT = 2.0

    def __init__(self):
        self._model: MapModel = InitialMapModel()
        self._model.save_point()
        self._view: QLabel | None = None
        self._status_bar: QStatusBar | None = None

    def set_view(self, view: QLabel) -> None:
        self._view = view

    def set_status_bar(self, status_bar: QStatusBar) -> None:
        self._status_bar = status_bar

    def  _post_update(self, future: Task[bytes]) -> None:
        data = future.result()
        if not data:
            return
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self._view.setPixmap(pixmap)

    async def update(self) -> None:
        if self._view is None:
            return

        size = self._view.size().width(), self._view.size().height()
        async with self._api as api:
            task = asyncio.create_task(api(self._model, size=size))
            task.add_done_callback(self._post_update)
            await task


    @staticmethod
    def update_decorator(function: Callable) -> Callable:
        @wraps(function)
        async def wrapper(self: 'MapController', *args, **kwargs) -> None:
            if self._status_bar:
                self._status_bar.showMessage('loading...')
            await function(self, *args, **kwargs)
            await self.update()
            if self._status_bar:
                self._status_bar.clearMessage()

        return wrapper

    def _change_scale(self, change: float) -> None:
        self._model.scale(change)

    @update_decorator
    async def scale_up(self) -> None:
        self._change_scale(self.SCALE_COEFFICIENT)

    @update_decorator
    async def scale_down(self) -> None:
        self._change_scale(1 / self.SCALE_COEFFICIENT)

    @update_decorator
    async def left(self) -> None:
        self._model.longitude -= self._model.spn[0]

    @update_decorator
    async def right(self) -> None:
        self._model.longitude += self._model.spn[0]

    @update_decorator
    async def up(self) -> None:
        self._model.latitude += self._model.spn[1]

    @update_decorator
    async def down(self) -> None:
        self._model.latitude -= self._model.spn[1]

    @update_decorator
    async def set_theme(self, is_dark_theme: bool) -> None:
        self._model.darkTheme = is_dark_theme
