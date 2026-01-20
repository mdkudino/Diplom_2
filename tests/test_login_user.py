import allure
import pytest
from utils import UserUtils
from data import Messages


class TestLoginUser:

    @allure.title('Проверка авторизации пользователя с валидными данными')
    @allure.description('Отправляем запрос на авторизацию в сервисе, проверяем ответ и удаляем пользователя')
    def test_user_login_successfull_with_valid_data(self, user):
        response = UserUtils.login_user(user[0])
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert response.json()["accessToken"]


    @allure.title('Проверка ошибки при авторизации пользователя с неверными данными')
    @allure.description('Отправляем запрос на авторизацию в сервисе с неверными данными и проверяем ответ')
    @pytest.mark.parametrize('incorrect_data', [
        "email", 
        "password"
    ])
    def test_user_null_login_failed(self, user, incorrect_data):
        user[0][incorrect_data] = "12345"
        response = UserUtils.login_user(user[0])
        assert response.status_code == 401
        assert response.json()["success"] == False
        assert response.json()['message'] == Messages.incorrect_credentials_message


    @allure.title('Проверка ошибки при авторизации пользователя без заполнения обязательных полей email/password')
    @allure.description('Отправляем запрос на авторизацию в сервисе без заполнения обязательных полей email/password \
                        и проверяем ответ')
    @pytest.mark.parametrize('empty_data', [
        "email", 
        "password"
    ])
    def test_user_login_without_parameters_failed(self, user, empty_data):
        user[0][empty_data] = ""
        response = UserUtils.login_user(user[0])
        assert response.status_code == 401
        assert response.json()["success"] == False
        assert response.json()['message'] == Messages.incorrect_credentials_message
    