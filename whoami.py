""" Whoami data """

class WhoAmI:
    """ Who Am I Class """
    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def first_name(self) -> str:
        return self._data['first_name']

    @property
    def last_name(self) -> str:
        return self._data['last_name']

    @property
    def email(self) -> str:
        return self._data['email']

    @property
    def id(self) -> str:
        return self._data['id']

    @property
    def type(self) -> str:
        return self._data['type']

    @property
    def json(self) -> str:
        return self._data

