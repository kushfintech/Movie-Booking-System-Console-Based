from typing import Optional
from models.customer_model import CustomerModel


class SeatModel:
    """
    SeatModel represents a seat within a movie session, including its reservation status
    and the customer who has booked it, if any.
    """

    def __init__(self, seat_number: int, is_reserved: bool = False,
                 booked_by: Optional[CustomerModel] = None):
        self.seat_number = seat_number
        self.is_reserved = is_reserved
        self.booked_by = booked_by

    def serialize(self):
        """Serialize the SeatModel instance to a dictionary."""
        return {
            'seat_number': self.seat_number,
            'is_reserved': self.is_reserved,
            'booked_by': self.booked_by.id if self.booked_by else None
        }

    @classmethod
    def deserialize(cls, data, all_customers):
        """
        Deserialize a dictionary back to a SeatModel instance.
        Uses the 'all_customers' list to reference the 'booked_by' attribute.
        """
        booked_by_id = data.get('booked_by')
        booked_by = next((cust for cust in all_customers if cust.id == booked_by_id), None)
        return cls(
            seat_number=data['seat_number'],
            is_reserved=data['is_reserved'],
            booked_by=booked_by
        )
