import os
from enum import Enum
import requests
import configparser


class RequestMethod(Enum):
    GET = 'GET'
    POST = 'POST'


class JSONResponse:
    def __init__(self, json, status_code):
        self._json = json
        self._status_code = status_code

    def __getitem__(self, item):
        return self._json[item]

    def __contains__(self, item):
        return item in self._json

    def __str__(self):
        return f'status = {self._status_code}, json = {self._json}'

    @property
    def status(self):
        return self._status_code


class JSONRequest:

    def __init__(self, method: RequestMethod, url: str, params: dict, headers: dict):
        self._method = method
        self._url = url
        self._params = params
        self._headers = headers

    def request(self) -> JSONResponse:
        response = requests.request(
            method=self._method.value,
            url=self._url,
            params=self._params,
            headers=self._headers)
        json = None
        try:
            json = response.json()
        except Exception as e:
            json = dict()
        return JSONResponse(json, response.status_code)


class JSONRequestBuilder: #Wzorzec projektowy - builder

    def __init__(self):
        self._headers = dict()
        self._params = dict()
        self._url = None
        self._method = None

    def with_method(self, method: RequestMethod):
        assert self._method is None
        self._method = method
        return self

    def for_url(self, url: str):
        assert self._url is None
        self._url = url
        return self

    def add_headers(self, headers: dict):
        self._headers.update(headers)
        return self

    def add_query_params(self, params: dict):
        self._params.update(params)
        return self

    def build(self):
        assert self._headers
        assert self._url
        assert self._method
        return JSONRequest(
            method=self._method,
            url=self._url,
            params=self._params,
            headers=self._headers
        )


class Configuration: #Wzorzec projektowy - adapter
    def __init__(self):
        self._config = configparser.ConfigParser()
        path = os.path.dirname(os.path.realpath(__file__))
        self._config.read(f'{path}\\..\\config.ini')

    def get_section(self, name: str):
        assert name in self._config
        return self._config[name]
