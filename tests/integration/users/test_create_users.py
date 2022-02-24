from rest_framework import status

from .test_users_setup import TestUsersSetUp
from apps.users.models import User

class CreateUsersTestUsers(TestUsersSetUp):

    def test_user_can_be_registered(self):
        res = self.client.post(self.register_url, self.user_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_user_cannot_be_registered_without_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_be_registered_with_existent_email(self):
        user = self.user_factory()
        self.user_data['email'] = user.email
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)





