import allure
from faker import Faker
import requests

from endpoints import Endpoints
from urls import Urls


class UserDataGenerator:
    
    @staticmethod
    @allure.step("Генерируем валидные фейковые данные для создания пользователя")
    def generate_fake_valid_user_data():
        fake = Faker("ru_RU")
        username = fake.user_name()
        password = fake.password()
        email = fake.email()
        data = {
            "email": email,
            "password": password,
            "name": username
        }
        return data
    
    @staticmethod
    @allure.step("Генерируем невалидные фейковые данные (отсутствуют обязательные поля) для создания пользователя")
    def generate_fake_invalid_user_data_no_field(contained_data):
        fake = Faker("ru_RU")
        data = {}
        if "name" in contained_data:
            name = fake.user_name()
            data["name"] = name
        if "password" in contained_data:
            password = fake.password()
            data["password"] = password
        if "email" in contained_data:
            email = fake.email()
            data["email"] = email
        return data

class UserUtils:

    @staticmethod
    @allure.step("Отправляем запрос на создание пользователя")
    def create_user(user_data):
        response = requests.post(f'{Urls.STELLAR_BURGER_URL}{Endpoints.create_user}', data=user_data)
        return response
    
    @staticmethod
    @allure.step("Отправляем запрос на удаление пользователя")
    def delete_user(access_token):
        del_response = requests.delete(f'{Urls.STELLAR_BURGER_URL}{Endpoints.create_user}{access_token}')
        return del_response
    
    @staticmethod
    @allure.step("Отправляем запрос на логин пользователя")
    def login_user(user_data):
        login_response = requests.post(f'{Urls.STELLAR_BURGER_URL}{Endpoints.login_user}', data=user_data)
        return login_response
    
    @staticmethod
    @allure.step("Получаем Access Token пользователя")
    def get_user_access_token(login_response):
        return login_response.json().get("accessToken")
    
    @staticmethod
    @allure.step("Получаем Refresh Token пользователя")
    def get_user_refresh_token(login_response):
        return login_response.json().get("refreshToken")
    
    @staticmethod
    @allure.step("Отправляем запрос выход из системы")
    def logout_user(refresh_tocken):
        logout_data = {"refreshTocken": refresh_tocken}
        logout_response = requests.post(f'{Urls.STELLAR_BURGER_URL}{Endpoints.logout_user}', data=logout_data)
        return logout_response
    
    

class OrderUtils:
    @staticmethod
    @allure.step("Отправляем запрос на получение списка доступных ингредиентов")
    def get_available_ingredients():
        response = requests.get(f'{Urls.STELLAR_BURGER_URL}{Endpoints.get_ingredients}')
        return response
    
    @staticmethod
    @allure.step("Отправляем запрос на создание заказа")
    def create_order(ingredients, access_token=None):
        header = None
        if access_token is not None:
            header = {"Authorization": access_token}
        request_data = {"ingredients": ingredients}
        response = requests.post(f'{Urls.STELLAR_BURGER_URL}{Endpoints.create_order}', data=request_data, headers=header)
        return response
    
    @staticmethod
    @allure.step("Отправляем запрос на получение списка заказов")
    def get_order_list(access_token=None):
        header = None
        if access_token is not None:
            header = {"Authorization": access_token}
        response = requests.get(f'{Urls.STELLAR_BURGER_URL}{Endpoints.get_orders}', headers=header)
        return response
    