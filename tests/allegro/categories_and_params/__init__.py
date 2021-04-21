from tests.allegro import APITestBase


class CategoriesAPITestBase(APITestBase):

    @classmethod
    def api_get(cls, url_part='', params=dict()):
        return super().api_get(f'/sale/categories{url_part}', params)