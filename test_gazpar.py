from calendar import month
from datetime import datetime, timedelta
from re import A
from .gazpar import Grdf
from api import GrdfApi
from gazpar import Gazpar
from aiohttp import ClientSession
import asyncio
import logging

# grdf = Grdf()
# grdf.login(username="comtchr@gmail.com", password="Sogamax60")
# account = grdf.getWhoami()
# pce = grdf.getPceList()

_LOGGER = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as session:
        gazpar = Gazpar(
            username="comtchr@gmail.com", password="Sogamax60", session=session
        )
        data = await gazpar.login()
        _LOGGER.info("Retour : %s", data)

        whoami = await gazpar.async_get_whoami()
        _LOGGER.info("Who Am I : %s %s", whoami.first_name, whoami.last_name)

        pce = await gazpar.async_get_pce()
        _LOGGER.info("PCE: %s", pce[0].json)

        end_date = datetime.today()
        start_date = end_date - timedelta(days=30)
        measures = await gazpar.async_get_conso(pce[0].pce, start_date, end_date)
        _LOGGER.info("Dernier index : %d", measures[-1].end_index)
        for measure in measures:
            _LOGGER.info(
                "%s : %d (%d)", measure.gas_date, measure.volume, measure.end_index
            )
        # data = await api.async_request(endpoint='e-conso/pce')
        # if data["status"] == 'success' :
        #    pce = data['data'][0]['idObject']
        #    _LOGGER.info("Get pce list\n%s",pce)


asyncio.run(main())
