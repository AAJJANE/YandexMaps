import asyncio
from asyncio import Task
from functools import wraps
from typing import Callable

from PyQt6.QtWidgets import QLineEdit

from src.static import MapController
from src.toponym.api import ToponymApi
from src.toponym.model import Toponym


class ToponymController:
    _api = ToponymApi()

    def __init__(self):
        self._model: Toponym | None = None
        self._output_view: QLineEdit | None = None
        self._static_controller: MapController | None = None
        self._query = ''

    def set_output_view(self, view: QLineEdit) -> None:
        self._output_view = view

    def set_static_controller(self, controller: MapController) -> None:
        self._static_controller = controller

    def _post_update(self, future: Task[Toponym | None]) -> None:
        self._model = future.result()
        if not self._model:
            self._output_view.clear()
        else:
            self._output_view.setText(str(self._model))

    async def update(self) -> None:
        if self._output_view is None:
            return

        async with self._api as api:
            task = asyncio.create_task(api.makeToponym(self._query))
            task.add_done_callback(self._post_update)
            await task
            if self._static_controller is not None:
                if self._model is None:
                    await self._static_controller.remove_point()
                else:
                    await self._static_controller.set_location(self._model.latitude, self._model.longitude)

    @staticmethod
    def update_decorator(function: Callable) -> Callable:
        @wraps(function)
        async def wrapper(self: 'ToponymController', *args, **kwargs) -> None:
            await function(self, *args, **kwargs)
            await self.update()

        return wrapper

    @update_decorator
    async def update_toponym(self, query: str) -> None:
        self._query = query.strip()
    
    def update_postal_code(self, is_show: bool) -> None:
        if self._model:
            self._model.set_show_postal_code(is_show)
            self._output_view.setText(str(self._model))
