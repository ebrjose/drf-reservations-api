from datetime import date, timedelta
import factory
from faker import Faker
from .room_factory import RoomFactory
from .user_factory import UserFactory


from apps.reservations.models import Reservation

fake = Faker()

class ReservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reservation

    room = factory.SubFactory(RoomFactory)
    guest = factory.SubFactory(UserFactory)
    checkin_date = date.today() + timedelta(days=1)
    checkout_date = date.today() + timedelta(days=3)
    status = 'PENDING'








