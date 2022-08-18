import requests
import logging
from faker import Faker

logger = logging.getLogger('api')
fake = Faker()


class RegisterUser:
    REGISTER_URL = '/api/v2/users/'
    LOGIN_URL = '/api/v2/users/login/'

    def register_user(self, url: str, body: dict):
        response = requests.post(url=f'{url}{self.REGISTER_URL}', json=body)
        logger.info(response.text)
        return response.json().get('user').get('token')

    def login_user(self, url: str, body: dict):
        response = requests.post(url=f'{url}{self.LOGIN_URL}', json=body)
        logger.info(response.text)
        return response.json().get('user').get('token')
