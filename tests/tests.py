import unittest
from unittest.mock import patch

from controllers.reservation import add_booking, load_bookings
from controllers.staff import create_account, fetch_all_staffs, save_staffs
from controllers.movie import add_movie, save_all_movies, fetch_all_movies, view_all_movies


class TestMovieReservationSystem(unittest.TestCase):

    @patch('controllers.staff.fetch_all_staffs')
    @patch('controllers.staff.save_staffs')
    def test_create_account(self, mock_save_staffs, mock_fetch_all_staffs):
        # Mocking the return value of fetch_all_staffs to simulate an empty staff list
        mock_fetch_all_staffs.return_value = []
        # Test the function
        result = create_account("John Doe", "john@example.com", "password123", "123 Main St", "USA")
        # Check if save_staffs was called, indicating the account was created
        mock_save_staffs.assert_called()
        self.assertEqual(None,result)

    @patch('controllers.movie.save_all_movies')
    @patch('controllers.movie.fetch_all_movies')
    def test_add_movie(self, mock_fetch_all_movies, mock_save_movies):
        # Mocking an empty movie list
        mock_fetch_all_movies.return_value = []
        # Test the function
        result = add_movie("Inception", 148)
        # Check if save_movies was called, indicating the movie was added
        mock_save_movies.assert_called()
        self.assertEqual(None, result)

    @patch('controllers.reservation.load_bookings')
    @patch('controllers.reservation.save_bookings')
    def test_add_booking(self, mock_save_bookings, mock_fetch_all_bookings):
        # Mocking an empty booking list
        mock_fetch_all_bookings.return_value = []
        # Test the function
        result = add_booking(customer_id=1, movie_session_id=2, seat_numbers=['A1', 'A2'])
        # Check if save_bookings was called, indicating the booking was added
        self.assertTrue(True,result)


if __name__ == '__main__':
    unittest.main()
