from django.db import models
from shortuuidfield import ShortUUIDField

from apps.base.models import BaseModel
from apps.reservations.models import Reservation
from apps.users.models import User

class Payment(BaseModel):
    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'CREDIT_CARD'
        CASH = 'CASH'
        PAYPAL = 'PAYPAL'

    uuid = ShortUUIDField()
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, verbose_name='Reservation ID', null=False)
    guest = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Guest ID', null=False)
    payment_method = models.CharField('Reservation State', max_length=20, choices=PaymentMethod.choices, null=False)
    taxes = models.DecimalField('Taxes', max_digits=10, decimal_places=2, null=False)
    room_charge = models.DecimalField('Room Charge', max_digits=10, decimal_places=2, null=False)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, null=False)
    payment_date = models.DateField('Payment Date', auto_now=False, auto_now_add=True, blank=False, null=False)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return self.uuid
