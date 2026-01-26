import pytest
from utils import UserDataGenerator, UserUtils, OrderUtils


@pytest.fixture()
def user_data():
    data = UserDataGenerator.generate_fake_valid_user_data()
    return data

@pytest.fixture()
def created_user(user_data):
    UserUtils.create_user(user_data)
    yield user_data

    login_response = UserUtils.login_user(user_data)
    access_token = UserUtils.get_user_access_token(login_response)
    UserUtils.delete_user(access_token)

@pytest.fixture()
def signed_in_user(created_user):
    login_response = UserUtils.login_user(created_user)
    access_token = UserUtils.get_user_access_token(login_response)
    yield access_token

    refresh_token = UserUtils.get_user_refresh_token(login_response)
    UserUtils.logout_user(refresh_token)

@pytest.fixture()
def ingredients():
   response = OrderUtils.get_available_ingredients()
   return response.json()['data']