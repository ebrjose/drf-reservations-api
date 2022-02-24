from rest_framework.test import APITestCase
from tests.factories.room_factory import RoomFactory

class TestRoomsSetUp(APITestCase):

    def setUp(self):
        self.url = '/api/rooms/'
        self.room_factory = RoomFactory
        self.room_data = {
            'type': 'SIMPLE',
            'description': 'A SIMPLE room',
            'price': 50
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


