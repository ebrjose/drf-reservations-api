from django.db import models
from shortuuidfield import ShortUUIDField

from apps.base.models import BaseModel
from apps.rooms.models import Room
from apps.users.models import User

class Reservation(BaseModel):
    class ReservationStatus(models.TextChoices):
        PENDING = 'PENDING'
        PAID = 'PAID'
        CANCELLED = 'CANCELLED'

    uuid = ShortUUIDField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Room ID', null=False)
    guest = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Guest ID', null=False)
    booking_date = models.DateTimeField('Reservation Date', auto_now=False, auto_now_add=True, blank=False, null=False)
    checkin_date = models.DateField('Check-In Date', auto_now=False, auto_now_add=False, blank=False, null=False)
    checkout_date = models.DateField('Check-Out Date', auto_now=False, auto_now_add=False, blank=False, null=False)
    status = models.CharField('Reservation State', max_length=10, choices=ReservationStatus.choices, default=ReservationStatus.PENDING)

    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    def __str__(self):
        return self.uuid

    def get_total_nights(self):
        diff = self.checkout_date - self.checkin_date
        return diff.days