from datetime import date, time, datetime


class ShowModel:
    def __init__(self, show_id: int, show_date: date, show_time: time):
        self.show_id: int = show_id
        self.show_date: date = show_date
        self.show_time: time = show_time

    def serialize(self):
        """Converts the Show instance to a dictionary for serialization."""
        return {
            'show_id': self.show_id,
            'show_date': self.show_date.strftime("%Y-%m-%d"),
            'show_time': self.show_time.strftime("%I:%M %p")
        }

    @classmethod
    def deserialize(cls, data: dict):
        """Creates a Show instance from a dictionary."""
        return cls(
            show_id=data.get('show_id', None),
            show_date=datetime.strptime(data['show_date'], "%Y-%m-%d").date(),
            show_time=datetime.strptime(data['show_time'], "%I:%M %p").time()
        )
