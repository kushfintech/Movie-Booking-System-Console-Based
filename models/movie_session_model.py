from typing import List
from models.seat_model import SeatModel
from models.show_model import ShowModel as ShowModel


class MovieSessionModel:
    """
    The MovieSessionModel class encapsulates all details of a movie session,
    including the seats, the show details, and the session status.
    """

    def __init__(self, session_id: int, movie_id: str, show: ShowModel,
                 seats: List[SeatModel], status: str = "AVAILABLE"):
        self.session_id = session_id
        self.movie_id = movie_id
        self.show = show
        self.seats = seats
        self.status = status

    def serialize(self):
        """Converts the MovieSessionModel instance to a dictionary for storage or transfer."""
        return {
            "session_id": self.session_id,
            "movie_id": self.movie_id,
            "seats": [seat.serialize() for seat in self.seats],
            "show": self.show.serialize(),
            "status": self.status
        }

    @classmethod
    def deserialize(cls, data, all_customers):
        """Reconstructs a MovieSessionModel instance from a dictionary."""
        seats = [SeatModel.deserialize(seat_data, all_customers) for seat_data in data['seats']]
        show = ShowModel.deserialize(data['show'])
        status = data.get('status', 'AVAILABLE')  # Default to 'AVAILABLE' if not specified
        return cls(
            session_id=data['session_id'],
            movie_id=data['movie_id'],
            seats=seats,
            show=show,
            status=status
        )
