from typing import List, Optional


class MovieModel:
    """
    The MovieModel class contains the attributes of a movie, such as its name,
    duration in minutes, a rating if provided, and the times it is being shown.
    """

    def __init__(self, movie_id: int, title: str, duration: int, rating: Optional[float] = None):
        self.movie_id = movie_id
        self.title = title
        self.duration = duration
        self.rating = rating

    def serialize(self):
        return {
            "movie_id": self.movie_id,
            "title": self.title,
            "duration": self.duration,
            "rating": self.rating,
        }

    @classmethod
    def deserialize(cls, data):
        movie_id = data['movie_id']
        title = data['title']
        duration = data['duration']
        rating = data.get('rating', None)
        return cls(movie_id, title, duration, rating)
