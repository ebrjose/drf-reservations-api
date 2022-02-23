from django.db import models
from django.db.models import fields
from rest_framework import serializers

from apps.payments.models import Payment
from apps.users.api.serializers import UserRegisterSerializer
from apps.reservations.api.serializers import ReservationListSerializer

class PaymentListSerializer(serializers.ModelSerializer):
    guest = serializers.StringRelatedField()
    reservation = serializers.StringRelatedField()
    class Meta:
        model = Payment
        fields = ('id', 'reservations', 'guest', 'payment_method', 'total', 'payment_date')


class ProccessPaymentSerializer(serializers.ModelSerializer):
    TAX_RATE = 0.13
    reservation = None

    class Meta:
        model = Payment
        fields = ('id', 'reservations', 'payment_method',)

    def create(self, validated_data):
        reservation = validated_data['reservations']
        self.update_booking_status(reservation)

        room_charge = self.calculate_room_charge(reservation)
        taxes =  self.calculate_taxes(room_charge)

        payment = Payment(**validated_data)
        payment.guest = reservation.guest
        payment.room_charge = room_charge
        payment.taxes = taxes
        payment.total = room_charge + taxes
        payment.save()

        return payment

    def update_booking_status(self, reservation):
        reservation.status = 'PAID'
        reservation.save()

    def calculate_room_charge(self, reservation):
        room_price = reservation.room.price
        return room_price * reservation.get_total_nights()

    def calculate_taxes(self, room_charge):
        return room_charge * self.TAX_RATE


class ViewPaymentSerializer(serializers.ModelSerializer):
    guest = UserRegisterSerializer()
    reservation = ReservationListSerializer()

    class Meta:
        model = Payment
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')