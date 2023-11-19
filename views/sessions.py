import inquirer

from controllers.movie_session import load_sessions, add_session
from controllers.movie import (get_movie_id_using_interactive_console,
                               get_movie_using_id,
                               )
from controllers.movie_session import (show_all_sessions, get_session_id_using_interactive_console,
                                       remove_session, add_show_date_time_for_movie, add_session,
                                       add_or_select_show_date, cancel_session
                                       )


def manage_sessions_menu():
    while True:
        print("\nManage Movies Sessions")
        menu_choices = [("Add Session", "1"), ("View All Sessions", "2"), ("Cancel Session", "3"),
                        ("Remove Session", "4"), ("Back", "5")]
        question = [
            inquirer.List('menu',
                          message="Select an Option:",
                          choices=menu_choices,
                          carousel=True)
        ]
        answers = inquirer.prompt(question)
        choice = answers['menu']
        if choice == "1":
            movie_id = get_movie_id_using_interactive_console()
            if movie_id:
                movie = get_movie_using_id(movie_id)
                print(movie.title)
                # Create Date
                show_date = add_or_select_show_date(movie_id)
                if show_date:
                    if show_date == "ADD_NEW":
                        date = input("Enter Date(YYYY-MM-DD): ")
                        time = input("Enter Time(HH:MM AM): ")
                        total_seats = input("Enter total seats: ")
                        add_session(movie_id=movie_id, total_seats=total_seats,
                                    show_date_str=date, show_time_str=time, )
                    elif show_date == "CANCEL":
                        pass
                    else:
                        print("Create New Show Time")
                        time = input("Enter Time(HH:MM AM): ")
                        total_seats = input("Enter total seats: ")
                        add_session(movie_id=movie_id, total_seats=total_seats,
                                    show_date_str=show_date, show_time_str=time, )

        if choice == "2":
            movie_id = get_movie_id_using_interactive_console()
            if movie_id:
                movie = get_movie_using_id(movie_id)
                print(f"Shows of {movie.title}")
                show_all_sessions()
        elif choice == "3":
            session_id = get_session_id_using_interactive_console()
            if session_id:
                cancel_session(session_id)
            return
        elif choice == "4":
            session_id = get_session_id_using_interactive_console()
            if session_id:
                remove_session(session_id)
            return
        elif choice == "5":
            return
        else:
            print("Invalid choice, please try again.")
