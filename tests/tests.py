from faker import Faker
import requests
import logging

from api import RegisterUser

URL = 'http://127.0.0.1:8000'
fake = Faker()
logger = logging.getLogger('tests')
reg_user = RegisterUser()


class TestRegistration:
    username = fake.user_name()
    email = fake.email()
    password = fake.password()
    body = {"user":
                {"username": username,
                 "password": password,
                 "email": email
                 }
            }

    def test_registration(self):
        """Тестируем регистрацию"""
        response = requests.post(url=f'{URL}/api/v2/users/', json=self.body)
        logger.info(response.text)
        assert response.status_code == 201
        assert response.json().get('user').get('username') == self.body['user']['username']
        assert response.json().get('user').get('email') == self.body['user']['email']
        assert response.json().get('user').get('role') == 'US'
        assert response.json().get('user').get('token') is not None

    def test_login(self, body=body):
        """Тестируем авторизацию"""
        response = requests.post(url=f'{URL}/api/v2/users/login/',
                                 json={"user": {
                                     "username": body.get('user').get('username'),
                                     "password": body.get('user').get('password')
                                 }})
        logger.info(response.text)
        assert response.status_code == 200
        assert response.json().get('user').get('username') == body.get('user').get('username')
        assert response.json().get('user').get('role') == 'US'


class TestApi:
    username = fake.user_name()
    email = fake.email()
    password = fake.password()
    body = {"user":
                {"username": username,
                 "password": password,
                 "email": email
                 }
            }

    def test_api_regions(self):
        token = reg_user.register_user(url=f'{URL}', body=self.body)
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(url=f'{URL}/api/v1/regions/', headers=headers)
        logger.info(response.text)
        assert response.status_code == 200

    def test_api_region(self):
        token = reg_user.login_user(url=f'{URL}', body=self.body)
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(url=f'{URL}/api/v1/region/Московская область/',
                                headers=headers)
        logger.info(response.text)
        assert response.status_code == 200

    def test_api_locality(self):
        token = reg_user.login_user(url=f'{URL}', body=self.body)
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(url=f'{URL}/api/v1/locality/',
                                headers=headers)
        logger.info(response.text)
        assert response.status_code == 200

    def test_api_locality_name(self):
        token = reg_user.login_user(url=f'{URL}', body=self.body)
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(url=f'{URL}/api/v1/locality/Апрелевка/',
                                headers=headers)
        logger.info(response.text)
        assert response.status_code == 200

    def test_api_inn(self):
        token = reg_user.login_user(url=f'{URL}', body=self.body)
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(url=f'{URL}/api/v1/inn/5024094889/',
                                headers=headers)
        logger.info(response.text)
        assert response.status_code == 200

    def test_api_categories(self):
        token = reg_user.login_user(url=f'{URL}', body=self.body)
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(url=f'{URL}/api/v1/categories/',
                                headers=headers)
        logger.info(response.text)
        assert response.status_code == 200

    def test_api_categories(self):
        token = reg_user.login_user(url=f'{URL}', body=self.body)
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(url=f'{URL}/api/v1/category/Автобусы/',
                                headers=headers)
        logger.info(response.text)
        assert response.status_code == 200

    def test_api_products(self):
        token = reg_user.login_user(url=f'{URL}', body=self.body)
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(url=f'{URL}/api/v1/products/',
                                headers=headers)
        logger.info(response.text)
        assert response.status_code == 200

    def test_api_product(self):
        token = reg_user.login_user(url=f'{URL}', body=self.body)
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(url=f'{URL}/api/v1/product/банки/',
                                headers=headers)
        logger.info(response.text)
        assert response.status_code == 200

    def test_api_id(self):
        token = reg_user.login_user(url=f'{URL}', body=self.body)
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(url=f'{URL}/api/v1/api_id/1/',
                                headers=headers)
        logger.info(response.text)
        assert response.status_code == 200

    def test_api_get_favourite(self):
        token = reg_user.login_user(url=f'{URL}', body=self.body)
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(url=f'{URL}/api/v1/favourite/',
                                headers=headers)
        logger.info(response.text)
        assert response.status_code == 200

    def test_api_post_favourite(self):
        token = reg_user.login_user(url=f'{URL}', body=self.body)
        headers = {'Authorization': f'Token {token}'}
        data = {"favourite": [1, 2]}
        response = requests.post(url=f'{URL}/api/v1/favourite/',
                                headers=headers, json=data)
        logger.info(response.text)
        assert response.status_code == 200

    def test_api_delete_favourite(self):
        token = reg_user.login_user(url=f'{URL}', body=self.body)
        headers = {'Authorization': f'Token {token}'}
        data = {"favourite": [1]}
        response = requests.delete(url=f'{URL}/api/v1/favourite/',
                                 headers=headers, json=data)
        logger.info(response.text)
        assert response.status_code == 200

    def test_api_find(self):
        token = reg_user.login_user(url=f'{URL}', body=self.body)
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(url=f'{URL}/api/v1/find/?find=корсарус',
                                   headers=headers)
        logger.info(response.text)
        assert response.status_code == 200

    def test_api_last(self):
        token = reg_user.login_user(url=f'{URL}', body=self.body)
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(url=f'{URL}/api/v1/last/',
                                headers=headers)
        logger.info(response.text)
        assert response.status_code == 200

    def test_api_quantity(self):
        token = reg_user.login_user(url=f'{URL}', body=self.body)
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(url=f'{URL}/api/v1/last/',
                                headers=headers)
        logger.info(response.text)
        assert response.status_code == 200

    def test_api_analitics_categories(self):
        token = reg_user.login_user(url=f'{URL}', body=self.body)
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(url=f'{URL}/api/v1/analitics/categories/',
                                headers=headers)
        logger.info(response.text)
        assert response.status_code == 200

    def test_api_analitics_directions(self):
        token = reg_user.login_user(url=f'{URL}', body=self.body)
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(url=f'{URL}/api/v1/analitics/directions/',
                                headers=headers)
        logger.info(response.text)
        assert response.status_code == 200

    def test_api_analitics_locality(self):
        token = reg_user.login_user(url=f'{URL}', body=self.body)
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(url=f'{URL}/api/v1/analitics/locality/',
                                headers=headers)
        logger.info(response.text)
        assert response.status_code == 200