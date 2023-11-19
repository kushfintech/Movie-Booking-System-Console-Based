import inquirer

from controllers.movie import (add_movie, delete_movie,
                               view_all_movies, fetch_all_movies, get_movie_id_using_interactive_console
                               )
from controllers.movie_session import select_show_date, select_show_time, display_seats_for_session

from controllers.reservation import (view_bookings, add_booking, show_booking_details_by_id,
                                     select_booking, cancel_booking, delete_booking)
from controllers.customer import get_cust_id


def reservation_menu():
    while True:
        print("\nMovie Reservation System")
        menu_choices = [("Add Movie", "1"), ("View All Movies", "2"), ("Remove Movie", "3"), ("Back", "4")]
        question = [
            inquirer.List('menu',
                          message="Select an Option:",
                          choices=menu_choices,
                          carousel=True)
        ]
        answers = inquirer.prompt(question)
        choice = answers['menu']
        if choice == "1":
            title = input("Enter movie title: ")
            duration = input("Enter movie duration(in minutes): ")
            showing_times = input("Enter showing times separated by comma without space between commas"
                                  " e.g. 2:30 PM,3:00 AM: ").split(',')
            add_movie(title=title, duration=duration)
        elif choice == "2":
            view_all_movies()
        elif choice == "3":
            movies = fetch_all_movies()
            if len(movies) > 0:
                view_all_movies()
                movie_id = int(input("Enter movie ID to remove: "))
                delete_movie(movie_id)
            else:
                print("Movies not Found for Delete.")

        elif choice == "4":
            break
        else:
            print("Bad choice! Try again.")


def manage_reservation_menu():
    while True:
        print("\nManage Reservations")
        menu_choices = [("View Reservations", "1"), ("Add New Reservation", "2"), ("Search Reservations", "3"),
                        ("Cancel Reservation", "4"), ("Delete Reservation", "5"), ("Back", "6")]
        question = [
            inquirer.List('menu',
                          message="Select an Option:",
                          choices=menu_choices,
                          carousel=True)
        ]
        answers = inquirer.prompt(question)
        choice = answers['menu']
        if choice == "1":
            view_bookings()
        elif choice == "2":
            movie_id = get_movie_id_using_interactive_console()
            if movie_id:
                show_date = select_show_date(movie_id)
                if show_date:
                    print("Select Show")
                    show_time = select_show_time(movie_id=movie_id, show_date_str=show_date)
                    if show_time:
                        session_id = display_seats_for_session(movie_id, show_date, show_time)
                        while True:
                            if session_id:
                                selected_seats = input("Enter seat numbers seperated by comma: ").split(',')
                                if len(selected_seats) > 0 and selected_seats[0] != "":
                                    customer_id = get_cust_id()
                                    result = add_booking(customer_id=customer_id, movie_session_id=session_id,
                                                         seat_numbers=selected_seats)
                                    if result:
                                        break

                                else:
                                    print("You didn't selected any seat")

        elif choice == "3":
            while True:
                print("Search for Reservations")
                reservation_id = input("Enter your reservation id in order to search or C to Cancel: ")
                if reservation_id:
                    if reservation_id.lower() == "c":
                        break
                    else:
                        show_booking_details_by_id(reservation_id)
        elif choice == "4":
            while True:
                print("Select Reservation to Cancel")
                reservation = select_booking()
                if reservation:
                    cancel_booking(reservation.booking_id)
                else:
                    break
        elif choice == "5":
            while True:
                print("Select Reservation to Delete")
                reservation = select_booking()
                if reservation:
                    delete_booking(reservation.booking_id)
                else:
                    break
        elif choice == "6":
            break
        else:
            print("Bad choice, please try again.")
