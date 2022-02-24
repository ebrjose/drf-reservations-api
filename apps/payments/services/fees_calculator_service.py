from apps.reservations.models import Reservation

class FeesCalculatorService:
    TAX_RATE = 0.13

    reservation = None
    room_charge = None
    taxes = None
    total = None

    def __init__(self, reservation: Reservation):
        self.reservation = reservation

    def calculate_room_charge(self):
        room_price = self.reservation.room.price
        return room_price * self.reservation.get_total_nights()

    def calculate_taxes(self):
        return self.calculate_room_charge() * self.TAX_RATE

    def calculate_total(self):
        return self.calculate_room_charge() + self.calculate_taxes()

    def total_fees(self):
        self.room_charge = self.calculate_room_charge()
        self.taxes = self.calculate_taxes()
        self.total = self.calculate_total()

        return self




