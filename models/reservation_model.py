from datetime import datetime
from typing import List

from models.customer_model import CustomerModel
from models.movie_session_model import MovieSessionModel
from models.seat_model import SeatModel


class BookingModel:
    def __init__(self, booking_id: int, customer: CustomerModel, movie_session: MovieSessionModel,
                 seats: List[SeatModel], reserved_time: datetime, booking_status: str = 'AVAILABLE'):
        self.booking_id = booking_id
        self.customer = customer
        self.movie_session = movie_session
        self.seats = seats
        self.reserved_time = reserved_time
        self.booking_status = booking_status

    def serialize(self):
        return {
            'booking_id': self.booking_id,
            'customer_id': self.customer.id,
            'session_id': self.movie_session.session_id,
            'seats': [seat.serialize() for seat in self.seats],
            'reserved_time': self.reserved_time.strftime("%Y-%m-%d %H:%M:%S"),
            'booking_status': self.booking_status,
        }

    @classmethod
    def deserialize(cls, data, all_customers, all_movie_sessions, all_seats):
        booking_id = data['booking_id']
        customer = next((cust for cust in all_customers if cust.id == data['customer_id']), None)
        movie_session = next((session for session in all_movie_sessions if session.session_id ==
                              data['session_id']), None)
        seats = [SeatModel.deserialize(seat_data, all_customers) for seat_data in data.get('seats', [])]
        reserved_time = datetime.strptime(data['reserved_time'], "%Y-%m-%d %H:%M:%S")
        booking_status = data['booking_status']

        return cls(booking_id, customer, movie_session, seats, reserved_time, booking_status)
