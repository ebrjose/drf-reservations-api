from django.db.models import fields
from rest_framework import serializers

from apps.reservations.models import Reservation
from apps.rooms.api.serializers import RoomSerializer
from apps.users.api.serializers import UserRegisterSerializer
from datetime import  date

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    def validate(self, data):

        if data['checkin_date'] < date.today():
            raise serializers.ValidationError(
                {'checkin_date':"""'checkin_date' must be greater than or equal to 'today'"""}
            )

        if data['checkin_date'] > data['checkout_date']:
            raise serializers.ValidationError(
                {'checkout_date':"""'checkout_date' must be greater than or equal to 'checkin_date'"""}
            )

        if not data['room'].available:
            raise serializers.ValidationError(
                {'room': """ Room is not available. """}
            )

        return data

    def create(self, validated_data):
        room = validated_data['room']
        room.available = False
        room.save()

        reservation = Reservation(**validated_data)
        reservation.save()

        return reservation


class ReservationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'uuid': instance.uuid,
            'reservation_date': instance.reservation_date,
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