# pylint: disable=too-many-public-methods
# pylint: disable=too-many-instance-attributes
""" Measure Data """
from .date_convert import date_from_grdf


class Measure:
    """Measure Class"""

    def __init__(self, pce, measure):
        # Init attribute
        self._data = measure
        self._pce = pce

    @property
    def start_date(self) -> str:
        return date_from_grdf(self._data["dateDebutReleve"])

    @property
    def end_date(self) -> str:
        return date_from_grdf(self._data["dateFinReleve"])

    @property
    def gas_date(self) -> str:
        return self._data["journeeGaziere"]

    @property
    def start_index(self) -> int:
        return self._data["indexDebut"]

    @property
    def end_index(self) -> int:
        return self._data["indexFin"]

    @property
    def volume(self) -> int:
        return self._data["volumeBrutConsomme"]

    @property
    def energy(self) -> int:
        return self._data["energieConsomme"]

    @property
    def conversion_factor(self) -> float:
        return self._data["coeffConversion"]

    @property
    def pce(self) -> str:
        return self._pce

    @property
    def json(self) -> str:
        return self._data
