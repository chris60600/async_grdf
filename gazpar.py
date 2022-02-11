""""""

from aiohttp import ClientSession

from whoami import WhoAmI
from pce import Pce
from api import GrdfApi

class Gazpar:
    """Main class for reading data from Grdf Api """

    def __init__(self, username, password, timeout: float = 1, session: ClientSession = None):

        if session is None:
            session = ClientSession()
            self._session = session
        self._username = username
        self._password = password
        self._pce_list = []
        self.api = GrdfApi(username=username, password=password, session=session)

    async def login(self):
        return await self.api.login()

    async def async_get_whoami(self) -> dict:
        """Get whoami data"""
        json_data = await self.api.async_request("e-connexion/users/whoami")
        if (json_data['status'] == 'success'):
            return WhoAmI(json_data['data'])

    async def async_get_pce(self) -> dict:
        """Get pce data"""
        json_data = await self.api.async_request('e-conso/pce')
        if (json_data['status'] == 'success'):
            pce_list = json_data['data']
            for item in pce_list:
                myPce = Pce(item)
                self._pce_list.append(myPce)

            return self._pce_list
