from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

from .api import MapApi
from .model import MapModel, InitialMapModel


class MapController:
    _api = MapApi()

    def __init__(self):
        self._model: MapModel = InitialMapModel()
        self._view: QLabel | None = None

    def set_view(self, view: QLabel) -> None:
        self._view = view

    def update(self) -> None:
        if self._view is None:
            return

        size = self._view.size().width(), self._view.size().height()
        data = self._api(self._model, size=size)
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self._view.setPixmap(pixmap)
