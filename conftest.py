import pytest
from utils import UserDataGenerator, UserUtils, OrderUtils


@pytest.fixture()
def user():
    data = UserDataGenerator.generate_fake_valid_user_data()
    UserUtils.create_user(data)
    login_response = UserUtils.login_user(data)
    access_token = UserUtils.get_user_access_token(login_response)
    yield [data, access_token]
    refresh_token = UserUtils.get_user_refresh_token(login_response)
    UserUtils.logout_user(refresh_token)
    UserUtils.delete_user(access_token)

@pytest.fixture()
def ingredients():
   response = OrderUtils.get_available_ingredients()
   return response.json()['data']