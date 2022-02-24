import random
from django.db import models

from apps.base.models import BaseModel

class Room(BaseModel):
    class RoomTypes(models.TextChoices):
        SIMPLE = 'SIMPLE'
        DOUBLE = 'DOUBLE'
        SUITE = 'SUITE'

    type = models.CharField('Room Type', max_length=10, choices=RoomTypes.choices, null=False)
    description = models.TextField('Description', blank=False, null=False)
    price = models.PositiveIntegerField('Price per night',default=10)
    available = models.BooleanField('Available', default=True)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return f"{self.id} | {self.type} | { 'Available' if self.available else 'Occupied' } | {self.description}"
