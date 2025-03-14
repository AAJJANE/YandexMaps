from dataclasses import dataclass
from typing import ClassVar

@dataclass
class MapModel:
    _latitude: float
    _longitude: float
    _spn: float
    darkTheme: bool = False
    _point: tuple[float, float] | None = None

    _MAX_LATITUDE: ClassVar[int] = 85

    @property
    def point(self) -> tuple[float, float] | None:
        return self._point

    def remove_point(self) -> None:
        self._point = None

    def save_point(self) -> None:
        self._point = self._longitude, self._latitude

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, value: float) -> None:
        if value >= self._MAX_LATITUDE - self.spn[1]:
            return
        if value <= -self._MAX_LATITUDE + self.spn[1]:
            return
        self._latitude = value

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, value: float) -> None:
        self._longitude = (value + 180) % 360 - 180

    @property
    def spn(self) -> tuple[float, float]:
        return self._spn, self._spn

    def scale(self, value: float) -> None:
        new_spn = self._spn * value
        if new_spn < 0.000125:  # Минимальный масштаб
            return
        if new_spn > 35:  # Максимальный масштаб
            return
        if self._MAX_LATITUDE - abs(self._latitude) < new_spn:
            return
        self._spn = new_spn


@dataclass
class InitialMapModel(MapModel):
    _latitude: float = 48.713945
    _longitude: float = 44.528397
    _spn: float = 0.002
