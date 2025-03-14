from functools import cached_property


class Toponym:
    def __init__(self, data):
        self._data = data

    @cached_property
    def latitude(self) -> float:
        return float(self._data["Point"]["pos"].split()[0])

    @cached_property
    def longitude(self) -> float:
        return float(self._data["Point"]["pos"].split()[1])

    @cached_property
    def address(self) -> str:
        return self._data["metaDataProperty"]["GeocoderMetaData"]["Address"]["formatted"]

    @cached_property
    def postal_code(self) -> str:
        return self._data["metaDataProperty"]["GeocoderMetaData"]["Address"].get("postal_code", "")
