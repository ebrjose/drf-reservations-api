from rest_framework.test import APITestCase
from tests.factories.user_factory import UserFactory

class TestUsersSetUp(APITestCase):

    def setUp(self):
        self.url = '/api/users/'
        self.register_url = '/api/users/register/'
        self.user_factory = UserFactory
        self.user_data = {
            'username' : 'testUser',
            'email' : 'test@mail.com',
            'name' : 'Test',
            'last_name' : 'User',
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


