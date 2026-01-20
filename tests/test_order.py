import allure
import pytest
import random
from utils import OrderUtils
from data import Messages

class TestOrder:

    @allure.title('Проверка создания заказа неавторизованным пользователем')
    @allure.description('Отправляем запрос на создание заказа для неавторизованного пользователя с разным числом ингредиентов')
    @pytest.mark.parametrize('num_ingredients', [1,2,3,4,5])
    def test_create_order_unauthorized_user_unauthorized_error(self, ingredients, num_ingredients):
       ingredients_order = [random.choice(ingredients)['_id'] for _ in range(num_ingredients)]
       response = OrderUtils.create_order(ingredients_order, "")
       assert response.status_code == 200
       assert(response.json()["success"] == True)
       assert(int(response.json()['order']['number']) > 0)

       response_orders = OrderUtils.get_order_list(None)
       assert response_orders.status_code == 401
       assert(response_orders.json()["success"] == False)
       assert(response_orders.json()["message"] == Messages.unauthorized_message)


    @allure.title('Проверка создания заказа авторизованным пользователем')
    @allure.description('Отправляем запрос на создание заказа для авторизованного пользователя с разным числом ингредиентов')
    @pytest.mark.parametrize('num_ingredients', [1,2,3,4,5])
    def test_create_order_authorized_user_success(self, user, ingredients, num_ingredients):
       ingredients_order = [random.choice(ingredients)['_id'] for _ in range(num_ingredients)]
       response = OrderUtils.create_order(ingredients_order, user[1])
       assert response.status_code == 200
       assert(response.json()["success"] == True)
       assert(int(response.json()['order']['number']) > 0)

       response_orders = OrderUtils.get_order_list(user[1])
       assert response_orders.status_code == 200
       assert(response_orders.json()["success"] == True)
       assert(response_orders.json()["orders"])

    @allure.title('Проверка создания заказа без ингредиентов')
    @allure.description('Отправляем запрос на создание заказа без ингредиентов')
    def test_create_order_wihout_ingredients_error(self):
       response = OrderUtils.create_order([], None)
       assert response.status_code == 400
       assert(response.json()["success"] == False)
       assert(response.json()["message"] == Messages.no_ingredients_message)


    @allure.title('Проверка создания заказа с неверным хэшем ингредиентов')
    @allure.description('Отправляем запрос на с разным числом ингредиентов с неверным хэшем')
    @pytest.mark.parametrize('num_ingredients', [1,2,3,4,5])
    def test_create_order_wrong_hash_error(self, ingredients, num_ingredients):
       ingredients_order = ["0" + random.choice(ingredients)['_id'][1:] for _ in range(num_ingredients)]
       response = OrderUtils.create_order(ingredients_order, None)
      
       assert response.status_code == 400
       assert(response.json()["success"] == False)
       assert(response.json()["message"] == Messages.incorrect_ingredient_hash_message)
