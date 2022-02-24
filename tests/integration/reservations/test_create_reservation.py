from datetime import date,timedelta
from rest_framework import status

from .test_reservations_setup import TestReservationsSetUp
from apps.rooms.models import Room

class CreateReservationsTest(TestReservationsSetUp):

    def test_room_can_be_unavailable_after_reservation(self):
        guest = self.guest_factory()
        room = self.room_factory()

        reservation_data = {
            'guest': guest.id,
            'room': room.id,
            'checkin_date': date.today(),
            'checkout_date': date.today() + timedelta(days=2),
        }

        response = self.client.post(self.url+'make/', reservation_data)
        room = Room.objects.get(pk=room.id)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(room.available)

    def test_cannot_make_a_reservation_without_data(self):
        response = self.client.post(self.url + 'make/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_checkin_date_must_be_greater_than_or_equal_to_today(self):
        guest = self.guest_factory()
        room = self.room_factory()

        reservation_data = {
            'guest': guest.id,
            'room': room.id,
            'checkin_date': date.today() - timedelta(days=1),
            'checkout_date': date.today() + timedelta(days=1),
        }

        response = self.client.post(self.url + 'make/', reservation_data)
        # import pdb; pdb.set_trace()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_checkout_date_must_be_greater_than_or_equal_to_checkin_date(self):
        guest = self.guest_factory()
        room = self.room_factory()

        reservation_data = {
            'guest': guest.id,
            'room': room.id,
            'checkin_date': date.today() ,
            'checkout_date': date.today() - timedelta(days=2),
        }

        response = self.client.post(self.url + 'make/', reservation_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_only_available_rooms_can_be_reserved(self):
        guest = self.guest_factory.create()
        room = self.room_factory.create(available=False)

        reservation_data = {
            'guest': guest.id,
            'room': room.id,
            'checkin_date': date.today(),
            'checkout_date': date.today() + timedelta(days=2),
        }

        response = self.client.post(self.url + 'make/', reservation_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

