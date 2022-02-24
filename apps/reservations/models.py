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
    reservation_date = models.DateTimeField('Reservation Date', auto_now=False, auto_now_add=True, blank=False, null=False)
    checkin_date = models.DateField('Check-In Date', auto_now=False, auto_now_add=False, blank=False, null=False)
    checkout_date = models.DateField('Check-Out Date', auto_now=False, auto_now_add=False, blank=False, null=False)
    status = models.CharField('Reservation State', max_length=10, choices=ReservationStatus.choices, default=ReservationStatus.PENDING)

    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    def __str__(self):
        return self.uuid

    def get_total_nights(self):
        diff = self.diff_days()
        return 1 if diff <= 0 else diff

    def diff_days(self):
        return (self.checkout_date - self.checkin_date).days