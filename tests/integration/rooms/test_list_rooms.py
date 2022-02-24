from rest_framework import status
from .test_rooms_setup import TestRoomsSetUp
from apps.rooms.models import Room

class ListRoomsTest(TestRoomsSetUp):

    def test_can_fetch_a_single_room(self):
        room = self.room_factory.create()
        response = self.client.get(f'{self.url}{room.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], room.id)

    def test_can_fetch_all_rooms(self):
        for _ in range(5):
            self.room_factory.create()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Room.objects.count(), 5)




