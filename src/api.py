import logging

import requests

from config import STATIC_MAPS_API

from .model import MapModel


TSize = tuple[int, int] | None


class MapApi:
    URL = 'https://static-maps.yandex.ru/v1?'

    @staticmethod
    def params(model: MapModel, size: TSize) -> dict:
        result = {
            'apikey': STATIC_MAPS_API,
            'll': '{},{}'.format(model.longitude, model.latitude),
            'spn': '{},{}'.format(*model.spn),
        }
        if size:
            scale_width = 1 if size[0] < 650 else size[0] / 650
            scale_height = 1 if size[1] < 450 else size[1] / 450
            scale = max(scale_width, scale_height)
            result['size'] = '{},{}'.format(
                int(size[0] / scale),
                int(size[1] / scale),
            )
        return result

    def __call__(self,
                 model: MapModel,
                 size: TSize = None
            ) -> bytes:
        response = requests.get(self.URL, params=self.params(model, size))
        print(response.url)
        return response.content
