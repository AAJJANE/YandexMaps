import aiohttp

from config import STATIC_MAPS_API

from .model import MapModel


TSize = tuple[int, int] | None


class MapApi:
    URL = 'https://static-maps.yandex.ru/v1?'

    def __init__(self):
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()

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

    async def __call__(self, model: MapModel, size: TSize = None) -> bytes:
        try:
            async with self.session.get(self.URL, params=self.params(model, size)) as response:
                print(response.url)
                return await response.read()
        except Exception:
            return
