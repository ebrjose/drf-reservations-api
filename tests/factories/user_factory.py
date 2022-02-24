import factory
from faker import Faker

from apps.users.models import User


fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.profile('username')['username'],
    email = fake.email(True)
    name = fake.first_name()
    last_name = fake.last_name()




