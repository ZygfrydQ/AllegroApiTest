import pytest

from tests.allegro.categories_and_params import CategoriesAPITestBase


@pytest.mark.api
class TestGetIdsAPI(CategoriesAPITestBase):

    def test_get_category_by_id(self):
        categoryId = 12
        response = self.api_get(f'/{categoryId}')
        assert response.status == 200, f"Request failed : {response}"
        assert response['id'] == '12', f"Returned id should match {categoryId} != {response['id']}"
        assert 'options' in response, "Response should have options"
        assert 'parent' in response, "Response should have parent"

    def test_not_existing_category(self):
        response = self.api_get(f'/{-100}')
        assert response.status == 404, f"Wrong status {response}"
        assert 'errors' in response, "Response should contain errors"
        errors = response['errors']
        assert len(errors) == 1, "There should be one error in response"
        error = errors[0]
        assert error['code'] == 'ERROR', "Wrong error code"
        assert error['details'] == 'ResourceNotFoundException', "Wrong error details"

