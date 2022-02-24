import random
import factory
from faker import Faker

from apps.rooms.models import Room

fake = Faker()

class RoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Room

    type = random.choice(['SIMPLE', 'DOUBLE', 'SUITE']),
    description = fake.sentence()
    price = fake.pyint(10, 100)
    available = True





