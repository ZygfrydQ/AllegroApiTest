import pytest
from pytest import fixture

from tests.allegro.categories_and_params import CategoriesAPITestBase


@pytest.mark.api
class TestGetCategoryAPI(CategoriesAPITestBase):

    @fixture(scope='class')
    def root_categories(self):
        response = self.api_get()
        assert response.status == 200, f"Request failed : {response}"
        assert 'categories' in response
        assert len(response['categories']) == 13
        return response['categories']

    def test_get_root_categories(self, root_categories):
        pass

    def test_traverse_category(self, root_categories):
        category_id = root_categories[0]['id']
        children_categories = self.api_get(params={'parent.id': category_id})
        assert children_categories.status == 200, f"Request failed : {children_categories}"
        assert 'categories' in children_categories, "Response should have categories."
        assert len(children_categories['categories']) > 0, "There should be at least one child category."

    def test_wrong_parent(self):
        response = self.api_get(params={'parent.id': -100})
        assert response.status == 404, f"Wrong status {response}"
        assert 'errors' in response, "Response should contain errors"
        errors = response['errors']
        assert len(errors) == 1, "There should be one error in response"
        error = errors[0]
        assert error['code'] == 'ERROR', "Wrong error code"
        assert error['details'] == 'ResourceNotFoundException', "Wrong error details"

