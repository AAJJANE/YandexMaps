import abc

import aiohttp


class AbstractApi(metaclass=abc.ABCMeta):
    URL = ''

    def __init__(self):
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()

    async def __call__(self, *args, **kwargs) -> bytes | None:
        try:
            async with self.session.get(
                    self.URL, params=self.params(*args, **kwargs)) as response:
                print(response.url)
                return await response.read()
        except Exception:
            return None

    @staticmethod
    @abc.abstractmethod
    def params(*args, **kwargs) -> dict:
        raise NotImplementedError
