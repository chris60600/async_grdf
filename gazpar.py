""" Reading Gazpar data from GRDF site API """

from datetime import datetime, timedelta
from aiohttp import ClientSession

from .whoami import WhoAmI
from .pce import Pce
from .measure import Measure
from .api import GrdfApi


class Gazpar:
    """Main class for reading data from Grdf Api"""

    def __init__(
        self,
        username,
        password,
        timeout: float = 1,
        session: ClientSession = None,
        out_json=False,
    ):

        if session is None:
            session = ClientSession()
            self._session = session
        self._username = username
        self._password = password
        self._out_json = out_json
        self._pce_list = []
        self._daily_measures = []
        self._daily_measures_json = {}
        self.api = GrdfApi(username=username, password=password, session=session)

    async def login(self):
        return await self.api.login()

    async def async_get_whoami(self) -> dict:
        """Get whoami data"""
        json_data = await self.api.async_request("e-connexion/users/whoami")
        if json_data["status"] == "success":
            return WhoAmI(json_data["data"])

    async def async_get_pce(self) -> dict:
        """Get pce data"""
        json_data = await self.api.async_request("e-conso/pce")
        if json_data["status"] == "success":
            pce_list = json_data["data"]
            for item in pce_list:
                pce = Pce(item)
                self._pce_list.append(pce)
            return self._pce_list

    async def async_get_conso(self, pce_id, start_date=None, end_date=None) -> dict:
        """Get pce data"""
        if end_date == None:
            end_date = datetime.today()
        if start_date == None:
            start_date = end_date - timedelta(days=30)

        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        route = f"e-conso/pce/consommation/informatives?dateDebut={start_date_str}&dateFin={end_date_str}&pceList%5B%5D={pce_id}"
        json_data = await self.api.async_request(route)
        if json_data["status"] == "success":
            measures = json_data["data"][pce_id]["releves"]
            for item in measures:
                measure = Measure(pce_id, item)
                self._daily_measures.append(measure)
                self._daily_measures_json[measure.gas_date] = measure.json
            if self._out_json:
                return json_data["data"]
            else:
                return self._daily_measures

    @property
    def measures_json(self):
        return self._daily_measures_json
