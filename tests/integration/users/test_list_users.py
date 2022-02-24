from rest_framework import status
from faker import Faker

from .test_users_setup import TestUsersSetUp
from apps.users.models import User

class ListUsersTest(TestUsersSetUp):

    def test_can_fetch_a_single_user(self):
        user = self.user_factory.create()
        response = self.client.get(f'{self.url}{user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], user.id)

    def test_can_fetch_all_rooms(self):
        fake = Faker()
        for _ in range(5):
            email=fake.company_email()
            username=email.split('@')[0]
            self.user_factory(email=email,username=username)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 5)




