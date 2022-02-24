from rest_framework import status

from .test_reservations_setup import TestReservationsSetUp
from apps.rooms.models import Room

class CreateReservationsTest(TestReservationsSetUp):

    def test_only_reservations_with_pending_status_can_be_cancelled(self):
        reservation = self.reservation_factory(status='PENDING')
        response = self.client.patch(f"{self.url}{reservation.id}/cancel/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_reservations_with_cancelled_status_cannot_be_cancelled(self):
        reservation = self.reservation_factory.create(status='CANCELLED')
        response = self.client.patch(f"{self.url}{reservation.id}/cancel/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reserved_room_changes_its_status_to_available_after_cancelling(self):
        room = self.room_factory(available=False)
        reservation = self.reservation_factory(room=room)
        self.assertEqual(reservation.room.available, False)
        response = self.client.patch(f"{self.url}{reservation.id}/cancel/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Room.objects.get(pk=room.id).available, True)




