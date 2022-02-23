from django.db.models import fields
from rest_framework import serializers

from apps.reservations.models import Reservation
from apps.rooms.api.serializers import RoomSerializer
from apps.users.api.serializers import UserRegisterSerializer

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class ReservationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'uuid': instance.uuid,
            'booking_date': instance.booking_date,
            'checkin_date': instance.checkin_date,
            'checkout_date': instance.checkout_date,
            'total_nights': instance.get_total_nights(),
            'guest': instance.guest.__str__(),
            'room': instance.room.__str__()
        }

class ReservationViewSerializer(serializers.ModelSerializer):
    guest = UserRegisterSerializer()
    room = RoomSerializer()
    class Meta:
        model = Reservation
        fields = '__all__'

class ReservationStatusSerializer(ReservationViewSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'status', 'guest')