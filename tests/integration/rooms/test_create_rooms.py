from rest_framework import status
from .test_rooms_setup import TestRoomsSetUp

class CreateRoomsTest(TestRoomsSetUp):

    def test_room_cannot_be_registered_without_data(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_room_can_be_registered_with_data(self):
        response = self.client.post(self.url, self.room_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], 1)

    def test_room_can_be_registered_without_field_type(self):
        response = self.client.post(self.url, { 'price': 50 })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




