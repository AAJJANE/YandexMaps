from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

from .api import MapApi
from .model import MapModel, InitialMapModel


class MapController:
    _api = MapApi()
    SCALE_COEFFICIENT = 2.0

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

    def _change_scale(self, change: float) -> float:
        self._model.scale(change)
        self.update()

    def scale_up(self) -> None:
        self._change_scale(self.SCALE_COEFFICIENT)

    def scale_down(self) -> None:
        self._change_scale(1 / self.SCALE_COEFFICIENT)

    def left(self) -> None:
        self._model.longitude -= self._model.spn[0]
        self.update()

    def right(self) -> None:
        self._model.longitude += self._model.spn[0]
        self.update()

    def up(self) -> None:
        self._model.latitude += self._model.spn[1]
        self.update()

    def down(self) -> None:
        self._model.latitude -= self._model.spn[1]
        self.update()
