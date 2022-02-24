from rest_framework.test import APITestCase

from tests.factories.room_factory import RoomFactory
from tests.factories.user_factory import UserFactory
from tests.factories.reservation_factory import ReservationFactory


class TestReservationsSetUp(APITestCase):

    def setUp(self):
        self.url = '/api/reservations/'

        self.room_factory = RoomFactory
        self.guest_factory = UserFactory
        self.reservation_factory = ReservationFactory

        return super().setUp()

    def tearDown(self):
        return super().tearDown()


