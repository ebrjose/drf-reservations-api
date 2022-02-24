from rest_framework.test import APITestCase
from tests.factories.reservation_factory import ReservationFactory

class TestPaymentsSetup(APITestCase):

    def setUp(self):
        self.url = '/api/payments/'
        self.process_url = '/api/payments/process/'
        self.reservation_factory = ReservationFactory

        return super().setUp()

    def tearDown(self):
        return super().tearDown()

