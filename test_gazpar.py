from re import A
from app.app.gazpar import Grdf
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
        gazpar = Gazpar(username="comtchr@gmail.com", password="Sogamax60",session=session)
        data = await gazpar.login()
        _LOGGER.info("Retour : %s",data)

        whoami = await gazpar.async_get_whoami()
        _LOGGER.info("Who Am I : %s %s",whoami.first_name, whoami.last_name)

        pce = await gazpar.async_get_pce()
        _LOGGER.info("PCE: %s",pce[0].json)
        #
        #data = await api.async_request(endpoint='e-conso/pce')
        #if data["status"] == 'success' :
        #    pce = data['data'][0]['idObject']
        #    _LOGGER.info("Get pce list\n%s",pce)


asyncio.run(main())