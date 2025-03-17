from typing import override
from json import loads

from config import GEOCODER_API
from src.absApi import AbstractApi
from src.toponym.model import Toponym


class ToponymApi(AbstractApi):
    URL = 'https://geocode-maps.yandex.ru/1.x/'

    @staticmethod
    @override
    def params(query: str) -> dict:
        result = {
            'apikey': GEOCODER_API,
            'format': 'json',
            'results': 1,
            'geocode': query
        }
        return result

    async def makeToponym(self, query: str) -> Toponym | None:
        if not query:
            return None
        data = await self(query)
        if data is None:
            return None
        try:
            data = loads(data.decode('utf-8'))
            data_obj = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
            return Toponym(data_obj)
        except Exception:
            return None
