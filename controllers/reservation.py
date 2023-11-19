import json
from datetime import datetime
from typing import List
import inquirer

from models.reservation_model import BookingModel
from controllers.customer import fetch_all_customers, get_customer_by_id
from controllers.movie import fetch_all_movies
from controllers.movie_session import (get_all_shows_of_all_sessions, load_sessions, get_movie_session_by_id,
                                       save_sessions)

RESERVATION_FILE = 'Reservations.dat'

def save_bookings(bookings: List[BookingModel]):
    try:
        bookings_data = [booking.serialize() for booking in bookings]

        with open(RESERVATION_FILE, 'w') as file:
            json.dump(bookings_data, file, indent=4)

        print("Bookings saved successfully.")
    except Exception as e:
        print(f"An error occurred while saving bookings: {e}")


def load_bookings():
    try:
        with open(RESERVATION_FILE, 'r') as f:
            bookings_data = json.load(f)

        all_customers = fetch_all_customers()
        all_movies_sessions = load_sessions()
        all_shows = get_all_shows_of_all_sessions()

        bookings = [
            BookingModel.deserialize(
                booking_data,
                all_customers,
                all_movies_sessions,
                all_shows
            ) for booking_data in bookings_data
        ]

        return bookings
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def view_bookings():
    bookings = load_bookings()

    if len(bookings) <= 0:
        print("No bookings found")
        return None

    headers = [
        "Booking ID", "Customer ID", "Customer Name", "Movie ID",
        "Movie Title", "Reserved Seats", "Show Date", "Show Time", "Reserved Datetime"
    ]

    all_customers = fetch_all_customers()
    all_movies = fetch_all_movies()

    rows = []
    for booking in bookings:
        customer = next((cust for cust in all_customers if cust.id == booking.customer.id), None)
        movie = next((mv for mv in all_movies if mv.movie_id == booking.movie_session.movie_id), None)

        row = {
            "Booking ID": booking.booking_id,
            "Customer ID": booking.customer.id,
            "Customer Name": customer.name if customer else "Unknown",
            "Movie ID": booking.movie_session.movie_id,
            "Movie Title": movie.title if movie else "Unknown",
            "Reserved Seats": [seat.seat_number for seat in booking.seats],
            "Show Date": booking.movie_session.show.show_date.strftime("%Y-%m-%d") if booking.movie_session.show else "N/A",
            "Show Time": booking.movie_session.show.show_time.strftime("%I:%M %p") if booking.movie_session.show else "N/A",
            "Reserved Datetime": booking.reserved_time.strftime("%Y-%m-%d %I:%M %p")
        }
        rows.append(row)

    column_widths = {header: max(len(header), max(len(str(row[header])) for row in rows)) for header in headers}

    header_row = " | ".join(header.ljust(column_widths[header]) for header in headers)
    print(header_row)
    print("-" * len(header_row))

    for row in rows:
        print(" | ".join(str(row[header]).ljust(column_widths[header]) for header in headers))


def generate_new_booking_id(bookings: List[BookingModel]):
    session_id = max(booking.booking_id for booking in bookings) + 1 if bookings else 1
    return session_id


def add_booking(customer_id, movie_session_id, seat_numbers):
    bookings = load_bookings()
    movie_sessions = load_sessions()

    movie_session = next((session for session in movie_sessions if session.session_id == movie_session_id), None)
    if movie_session is None:
        print(f"No movie session found with ID {movie_session_id}")
        return False

    selected_seats = []
    for seat in movie_session.seats:
        if str(seat.seat_number) in seat_numbers:
            if seat.is_reserved:
                print(f"Seat {seat.seat_number} is already reserved.")
                return False
            else:
                seat.is_reserved = True
                seat.booked_by = get_customer_by_id(customer_id)
                selected_seats.append(seat)

    booking_id = generate_new_booking_id(bookings)

    new_booking = BookingModel(
        booking_id=booking_id,
        customer=get_customer_by_id(customer_id),
        movie_session=get_movie_session_by_id(movie_session_id),
        seats=selected_seats,
        reserved_time=datetime.now(),
        booking_status="RESERVED"
    )
    bookings.append(new_booking)

    save_bookings(bookings)
    save_sessions(movie_sessions)

    print(f"Booking added successfully with no {new_booking.booking_id}.")
    return True


def cancel_booking(booking_id):
    bookings = load_bookings()
    movie_sessions = load_sessions()

    booking = next((res for res in bookings if res.booking_id == booking_id), None)
    if booking is None:
        print(f"No Booking found with ID {booking_id}")
        return False

    booking.status = 'CANCELLED'

    movie_session = next((session for session in movie_sessions if session.session_id ==
                          booking.movie_session.session_id),
                         None)
    if not movie_session:
        print(f"No movie session found for booking ID {booking_id}")
        return False

    for seat in movie_session.seats:
        if seat.seat_number in [s.seat_number for s in booking.seats]:
            seat.is_reserved = False

    save_bookings(bookings)
    save_sessions(movie_sessions)

    print("Booking cancelled successfully.")
    return True


def check_and_show_booking_details_of_customer(booking_id, customer_id):
    bookings = load_bookings()
    customers = fetch_all_customers()
    movie_sessions = load_sessions()

    booking = next((r for r in bookings if r.booking_id == booking_id), None)
    if not booking or booking.customer.id != customer_id:
        print(f"No valid booking found for booking ID: {booking_id} and Customer ID: {customer_id}")
        return

    customer = next((c for c in customers if c.id == customer_id), None)
    movie_session = next((ms for ms in movie_sessions if ms.session_id == booking.movie_session.session_id), None)

    if not customer or not movie_session:
        print("Error fetching booking details.")
        return

    headers = ["Booking ID", "Customer ID", "Customer Name", "Movie Title", "Session Date", "Session Time", "Seats", "Availability", "Booked By"]
    booking_data = {
        "Booking ID": booking.booking_id,
        "Customer ID": customer.id,
        "Customer Name": customer.name,
        "Movie Title": movie_session.movie.title,
        "Session Date": movie_session.show.show_date.strftime("%Y-%m-%d"),
        "Session Time": movie_session.show.show_time.strftime("%I:%M %p"),
        "Seats": ", ".join([seat.seat_number for seat in booking.seats_reserved]),
        "Availability": "RESERVED" if all(seat.is_reserved for seat in booking.seats_reserved) else "AVAILABLE",
        "Booked By": customer.name
    }

    column_widths = {header: max(len(header), len(str(booking_data[header]))) for header in headers}

    header_row = " | ".join(header.ljust(column_widths[header]) for header in headers)
    print(header_row)
    print("-" * len(header_row))

    row = " | ".join(str(booking_data[header]).ljust(column_widths[header]) for header in headers)
    print(row)


def show_booking_details_by_id(booking_id):
    bookings = load_bookings()
    customers = fetch_all_customers()
    movie_sessions = load_sessions()
    all_movies = fetch_all_movies()

    booking = next((r for r in bookings if str(r.booking_id) == booking_id), None)
    if not booking:
        print(f"No booking found for booking ID: {booking_id}")
        return

    customer = next((c for c in customers if c.id == booking.customer.id), None)
    movie_session = next((ms for ms in movie_sessions if ms.session_id == booking.movie_session.session_id), None)
    movie = next((mv for mv in all_movies if mv.movie_id == booking.movie_session.movie_id), None)

    if not customer or not movie_session:
        print("Error fetching booking details.")
        return

    booking_data = {
        "Booking ID": booking.booking_id,
        "Customer ID": booking.customer.id,
        "Customer Name": customer.name if customer else "Unknown",
        "Movie ID": booking.movie_session.movie_id,
        "Movie Title": movie.title if movie else "Unknown",
        "Reserved Seats": [seat.seat_number for seat in booking.seats],
        "Show Date": booking.movie_session.show.show_date.strftime(
            "%Y-%m-%d") if booking.movie_session.show else "N/A",
        "Show Time": booking.movie_session.show.show_time.strftime(
            "%I:%M %p") if booking.movie_session.show else "N/A",
        "Reserved Datetime": booking.reserved_time.strftime("%Y-%m-%d %I:%M %p")
    }

    # Print table
    headers = booking_data.keys()
    column_widths = {header: max(len(header), len(str(booking_data[header]))) for header in headers}
    header_row = " | ".join(header.ljust(column_widths[header]) for header in headers)
    print(header_row)
    print("-" * len(header_row))
    row = " | ".join(str(booking_data[header]).ljust(column_widths[header]) for header in headers)
    print(row)


def select_booking():
    bookings = load_bookings()
    all_movies = fetch_all_movies()

    if not bookings:
        print("No bookings found.")
        return None

    booking_choices = [
        (f"ID: {res.booking_id}, Date: {res.movie_session.show.show_date}, "
         f"Time: {res.movie_session.show.show_time},"
         f"Customer: {res.customer.name}", res.booking_id)
        for res in bookings
    ]

    post_special_options = [("Cancel", "CANCEL")]
    choices = booking_choices + post_special_options

    question = [
        inquirer.List('booking',
                      message="Select a booking:",
                      choices=choices,
                      carousel=True)
    ]

    # Prompt the user to choose a booking
    answers = inquirer.prompt(question)

    # Find and return the selected booking
    selected_booking_id = answers['booking']
    if selected_booking_id == "CANCEL":
        return None
    else:
        return next((res for res in bookings if res.booking_id == selected_booking_id), None)


def delete_booking(booking_id):
    # Load existing bookings
    bookings = load_bookings()  # Make sure this function is defined to load bookings

    # Find and remove the booking with the given ID
    bookings = [res for res in bookings if res.booking_id != booking_id]

    # Save the updated list of bookings
    save_bookings(bookings)  # Make sure this function is defined to save bookings

    print(f"Booking with ID {booking_id} has been removed.")
