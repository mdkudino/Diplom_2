import allure
import pytest
from utils import UserDataGenerator, UserUtils
from data import Messages

class TestCreateUser:

    @allure.title('Проверка ручки создания нового пользователя')
    @allure.description('Отправляем запрос на создание пользователя, проверяем ответ и удаляем созданного пользователя')
    def test_registration_user_successfull_with_valid_data(self):
        user_data = UserDataGenerator.generate_fake_valid_user_data()
        response = UserUtils.create_user(user_data)
        assert response.status_code == 200
        assert response.json()["success"] == True
        access_tocken = response.json()["accessToken"]
        UserUtils.delete_user(access_tocken)


    @allure.title('Проверка ошибки при при создании нового пользователя, который уже создан')
    @allure.description('Отправляем повторный запрос на создание пользователя, проверяем ответ и удаляем пользователя')
    def test_registration_double_user_failed(self):
        user_data = UserDataGenerator.generate_fake_valid_user_data()
        response = UserUtils.create_user(user_data)

        assert response.status_code == 200
        assert response.json()["success"] == True
        access_tocken = response.json()["accessToken"]

        response_second = UserUtils.create_user(user_data)

        assert response_second.status_code == 403
        assert response_second.json()["message"] == Messages.double_registration_message
        
        UserUtils.delete_user(access_tocken)

    @allure.title('Проверка ошибки при создании пользователя с отсутствующими обязательными полями')
    @allure.description('Отправляем запрос без обязательных полей и проверяем ошибку')
    @pytest.mark.parametrize('contained_data', [
        ["name"], 
        ["password"],
        ["email"]
    ])
    def test_registration_user_without_parameters_failed(self, contained_data):
        user_data = UserDataGenerator.generate_fake_invalid_user_data_no_field(contained_data)
        response = UserUtils.create_user(user_data)
        assert response.status_code == 403
        assert response.json()['message'] == Messages.not_enough_data_to_create_user_message