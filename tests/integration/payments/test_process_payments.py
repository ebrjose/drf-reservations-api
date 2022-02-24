from rest_framework import status

from .test_payments_setup import TestPaymentsSetup
from apps.payments.models import Payment
from apps.payments.services.fees_calculator_service import FeesCalculatorService

class TestsProcessPayments(TestPaymentsSetup):

    def test_process_payment(self):
        reservation = self.reservation_factory()
        total_fees = FeesCalculatorService(reservation).total_fees()

        process_data = {
            'reservation': reservation.id,
            'payment_method': 'CREDIT_CARD',
            'total': total_fees.total
        }
        response = self.client.post(self.process_url, process_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_wrong_amount_should_not_process_the_payment(self):
        reservation = self.reservation_factory()

        process_data = {
            'reservation': reservation.id,
            'payment_method': 'CREDIT_CARD',
            'total': 0
        }

        response = self.client.post(self.process_url, process_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



