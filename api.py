""" GRDF Gazpar API """
from __future__ import annotations
from dataclasses import dataclass

import datetime
from difflib import restore

import json
from json.decoder import JSONDecodeError

from math import fabs
from operator import rshift

from aiohttp import ClientSession, ClientTimeout, ClientResponse, ServerDisconnectedError
import aiohttp

import requests
from functools import wraps
import time

from exceptions import (
    GrdfApiDecodeError,
    GrdfApiConnectionTimeoutError,
    GrdfApiConnectionError
)

BASE_URL="monespace.grdf.fr"
DEFAULT_REQUEST_TIMEOUT: int=30

class GrdfApi:
    def __init__(self, username, password, session: ClientSession = None):
        """Init gazpar class

        Args:
            username: username
            password: password
            pce: Pce identifier
        """
        self.username = username
        self.password = password
        self.auth_nonce = None
        self._session = ClientSession = session
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Mobile Safari/537.36',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept':'application/json, */*',
            'Connection': 'keep-alive',
            'Referer': "https://monespace.grdf.fr/client/"
        }

    def get_url(self, endpoint: str):
        """Construct a Grdf Api URL for a specified endpoint"""
        return f"https://{BASE_URL}/api/{endpoint}"

    # Login
    async def login(self):
        """ Login to Grdf Web Site """

        use_running_session = self._session and not self._session.closed

        session: ClientSession
        if use_running_session:
            session = self._session
        else:
            session = ClientSession(
                timeout=ClientTimeout(total=DEFAULT_REQUEST_TIMEOUT),
                headers=self._headers
            )


        # Get cookie
        async with session.get(
            url=f'https://{BASE_URL}/client/particulier/accueil'
        ) as resp: 
            data = await resp.text()
 
        # if not 'auth_nonce' in self._session.cookie_jar._cookies["monespace.grdf.fr"]:
        #     _LOGGER.error("Cannot get auth_nonce.")
        # else:
        #     _LOGGER.debug("Cookies ok.")
        #     self.auth_nonce = self._session.cookie_jar._cookies["monespace.grdf.fr"]['auth_nonce']

        payload = {
            'email': self.username,
            'password': self.password,
            'capp': 'meg',
            'goto': 'https://sofa-connexion.grdf.fr:443/openam/oauth2/externeGrdf/authorize'
        }

        try:
            async with session.post(url='https://login.monespace.grdf.fr/sofit-account-api/api/v1/auth',data=payload
            ) as resp:
                response_json = await resp.json(content_type=None)
        except json.JSONDecodeError:
            response_text = await resp.text()
            data = {"status": "fail", "data": {"message": response_text}}
            return data
        except ServerDisconnectedError:
            data = {"status": "fail", "data": {"message": "Server Disconnected Error"}}
            use_running_session = False
        finally:
            if not use_running_session:
                await session.close()
                return


        if response_json['state'] != 'SUCCESS':
            data = {"status": "error", "data": response_json}
            await session.close()
            return data
        
 
        # Call whoami, this seems to complete _LOGGER. First time it fails then it is working. Don't call ugly things anymore
        try:
            async with session.get(url='https://monespace.grdf.fr/api/e-connexion/users/whoami'
            ) as resp:
                response_json = await resp.json(content_type=None)
        except json.JSONDecodeError:
            response_text = await resp.text()
            data = {"status": "warning", "data": response_json}
            return data
        except Exception as e:
            data = {"status": "fail", "data": {"message": str(e)}}
            return data
        
        # When everything is ok
        self.isConnected = True
    

    async def async_request(self, endpoint: str) -> dict:
        session = self._session
        try:
            async with session.get(url=self.get_url(endpoint)
            ) as resp:
                resp.raise_for_status()
                return await self.decode_response(resp)
        except aiohttp.ClientError as ex:
            raise GrdfApiConnectionError(
                f"Error while communicating with Grdf Api at {endpoint}: {ex}"
            ) from ex


    async def decode_response(self, response: ClientResponse) -> dict:
        """Decode response applying potentially needed workarounds."""
        raw_body = await response.text()
        try:
            response_json = json.loads(raw_body)
            data = {"status": "success", "data": response_json}
            return data
        except JSONDecodeError as ex:
            data = {"status": "Error", "data": {"message": "Error decoding json data"}}
            return data
#
#---------------------------------------------------------------------------------------
#   Obsolete
#---------------------------------------------------------------------------------------

    async def get_whoami(self):

        session = self._session

        try:
            async with session.get(url='https://monespace.grdf.fr/api/e-connexion/users/whoami'
            ) as resp:
                response_json = await resp.json(content_type=None)
                data = {"status": "success", "data": response_json}
        except json.JSONDecodeError:
            data = {"status": "Error", "data": {"message": "Error decoding json data","method": "getWhoiam"}}
            self.isConnected = False
        except Exception as e:
            data = {"status": "fail", "data": {"message": str(e)}}
            self.isConnected = False
        finally:
            return data

    async def get_pce_list(self):

        session = self._session
       
        # Get PCEs from website
        try:
            async with session.get(url='https://monespace.grdf.fr/api/e-conso/pce'
            ) as resp:
                response_json = await resp.json(content_type=None)
                data = {"status": "success", "data": response_json}
        except json.JSONDecodeError:
            data = {"status": "Error", "data": {"message": "Error decoding json data","method": "get_pce_list"}}
            self.isConnected = False
        except Exception as e:
            data = {"status": "fail", "data": {"message": str(e)}}
            self.isConnected = False
        finally:
            return data


