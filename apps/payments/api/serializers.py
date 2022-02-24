from rest_framework import serializers

from apps.payments.models import Payment
from apps.users.api.serializers import UserRegisterSerializer
from apps.reservations.api.serializers import ReservationListSerializer
from apps.payments.services.fees_calculator_service import FeesCalculatorService

class PaymentListSerializer(serializers.ModelSerializer):
    guest = serializers.StringRelatedField()
    reservation = serializers.StringRelatedField()
    class Meta:
        model = Payment
        fields = ('id', 'reservation', 'guest', 'payment_method', 'total', 'payment_date')


class ProcessPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ('id', 'reservation', 'payment_method', 'total')

    def validate(self, data):
        reservation = data['reservation']
        total_fees = FeesCalculatorService(reservation).total_fees()

        if reservation.status != 'PENDING':
            raise serializers.ValidationError(
                {'reservation': f"""The reservation has been {reservation.status}, the payment cannot be processed."""}
            )

        if float(data['total']) != float(total_fees.total):
            raise serializers.ValidationError(
                {'total': f"""'Total amount must be equal to '{total_fees.total}', the payment cannot be processed."""}
            )

        return data

    def create(self, validated_data):
        reservation = validated_data['reservation']

        total_fees = FeesCalculatorService(reservation).total_fees()

        self.update_reservation_status(reservation)
        self.set_room_available(reservation)

        payment = Payment(**validated_data)
        payment.guest = reservation.guest
        payment.room_charge = total_fees.room_charge
        payment.taxes = total_fees.taxes
        payment.total = total_fees.total
        payment.save()

        return payment

    def update_reservation_status(self, reservation):
        reservation.status = 'PAID'
        reservation.save()

    def set_room_available(self, reservation):
        room = reservation.room
        room.available = True
        room.save()


class ViewPaymentSerializer(serializers.ModelSerializer):
    guest = UserRegisterSerializer()
    reservation = ReservationListSerializer()

    class Meta:
        model = Payment
        exclude = ('active', 'created_date', 'modified_date', 'deleted_date')