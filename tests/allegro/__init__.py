import base64

import pytest

from tests import JSONRequestBuilder, RequestMethod, Configuration


class APISettings:
    def __init__(self, token_url, api_url, client_id, client_token):
        self.token_url = token_url
        self.api_url = api_url
        self.client_id = client_id
        self.client_token = client_token


@pytest.mark.api
class APITestBase:
    @classmethod
    def __get_api_token(cls):
        client_id = cls._api_settings.client_id
        token = cls._api_settings.client_token

        auth = str(base64.b64encode(bytes(f'{client_id}:{token}', 'utf-8')), 'utf-8')

        return JSONRequestBuilder() \
            .for_url(cls._api_settings.token_url) \
            .with_method(RequestMethod.POST) \
            .add_query_params({'grant_type': 'client_credentials'}) \
            .add_headers({'Authorization': f'Basic {auth}'}) \
            .build() \
            .request()['access_token']

    @classmethod
    def setup_class(cls):
        config = Configuration()
        api_section = config.get_section('API')
        cls._api_settings = APISettings(api_section['token_url'], api_section['api_url'], api_section['client_id'],
                                        api_section['client_token'])
        cls._api_token = cls.__get_api_token()

    @classmethod
    def api_get(cls, url_part: str, params=dict()):
        return JSONRequestBuilder() \
            .for_url(f'{cls._api_settings.api_url}{url_part}') \
            .with_method(RequestMethod.GET) \
            .add_query_params(params) \
            .add_headers({
            'Authorization': f'Bearer {cls._api_token}',
            'Accept': 'application/vnd.allegro.public.v1+json'
        }).build() \
            .request()
