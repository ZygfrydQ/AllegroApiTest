import pytest

from tests.allegro.categories_and_params import CategoriesAPITestBase


@pytest.mark.api
class TestGetParametersAPI(CategoriesAPITestBase):

    def test_get_parameters_for_category(self):
        categoryId = 12
        response = self.api_get(f'/{categoryId}/parameters')
        assert response.status == 200, f"Request failed : {response}"
        assert 'parameters' in response, "Response should have parameters"
        parameters = response['parameters']
        assert len(parameters) > 0, "There should be at least one parameter in response"
        for param in parameters:
            assert param, "Empty parameter in result"
            assert 'id' in param, "Each parameter should have id"
            assert 'name' in param, "Each parameter should have name"
            assert 'type' in param, "Each parameter should have type"

    def test_get_parameters_not_existing_category(self):
        categoryId = -100
        response = self.api_get(f'/{categoryId}/parameters')
        assert response.status == 404, f"Wrong status {response}"
        assert 'errors' in response, "Response should contain errors"
        errors = response['errors']
        assert len(errors) == 1, "There should be one error in response"
        error = errors[0]
        assert error['code'] == 'ERROR', "Wrong error code"
        assert error['details'] == 'ResourceNotFoundException', "Wrong error details"

