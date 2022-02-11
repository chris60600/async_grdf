class Pce:
    """ PCE Class """
    def __init__(self, item: dict) -> None:
        self._data = item

    @property
    def pce(self) -> str:
        return self._data['pce']

    @property
    def alias(self) -> str:
        return self._data['alias']

    @property
    def freq(self) -> str:
        return self._data['frequenceReleve']

    @property
    def collect_date(self) -> str:
        return self._data['dateDerniereVerification']

    @property
    def activation_date(self) -> str:
        return self._data['dateActivation']

    @property
    def state(self) -> str:
        return self._data['etat']

    @property
    def owner_name(self) -> str:
        return self._data['nomTitulaire']

    @property
    def postal_code(self) -> str:
        return self._data['codePostal']

    @property
    def json(self) -> str:
        return self._data

