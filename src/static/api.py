from typing import override

from config import STATIC_MAPS_API
from src.absApi import AbstractApi

from src.static.model import MapModel


TSize = tuple[int, int] | None


class MapApi(AbstractApi):
    URL = 'https://static-maps.yandex.ru/v1?'


    @staticmethod
    @override
    def params(model: MapModel, size: TSize) -> dict:
        result = {
            'apikey': STATIC_MAPS_API,
            'll': '{},{}'.format(model.longitude, model.latitude),
            'spn': '{},{}'.format(*model.spn),
            'theme': 'dark' if model.darkTheme else 'light',
        }
        if model.point:
            coords = '{},{}'.format(*model.point)
            result['pt'] = coords + ',comma'
        if size:
            scale_width = 1 if size[0] < 650 else size[0] / 650
            scale_height = 1 if size[1] < 450 else size[1] / 450
            scale = max(scale_width, scale_height)
            result['size'] = '{},{}'.format(
                int(size[0] / scale),
                int(size[1] / scale),
            )
        return result

