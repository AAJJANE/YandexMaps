from dataclasses import dataclass

@dataclass
class MapModel:
    _latitude: float
    _longitude: float
    _spn: float

    @property
    def latitude(self) -> float:
        return self._latitude

    @property
    def longitude(self) -> float:
        return self._longitude

    @property
    def spn(self) -> tuple[float, float]:
        return self._spn, self._spn


@dataclass
class InitialMapModel(MapModel):
    _latitude: float = 48.713945
    _longitude: float = 44.528397
    _spn: float = 0.002
