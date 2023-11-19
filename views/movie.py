import inquirer

from controllers.movie import (add_movie, delete_movie, update_movie,
                               view_all_movies, fetch_all_movies, get_movie_id_using_interactive_console)


def manage_movie_menu():
    while True:

        movie_choices = [("Add Movie", "1"), ("View All Movies", "2"), ("Update Movie", "3"), ("Remove Movie", "4"),
                         ("Cancel", "5")]

        question = [
            inquirer.List('manage_movie_menu',
                          message="Select an Option:",
                          choices=movie_choices,
                          carousel=True)
        ]

        answers = inquirer.prompt(question)

        choice = answers['manage_movie_menu']
        if choice == "1":
            title = input("Enter movie title: ")
            duration = input("Enter movie duration(in minutes): ")
            add_movie(title=title, duration=duration)
        elif choice == "2":
            view_all_movies()
        elif choice == "3":
            print("Which movie would you like to update?")
            movie_id = get_movie_id_using_interactive_console()
            if movie_id:
                title = input("Enter movie title: ")
                duration = input("Enter movie duration(in minutes): ")
                update_movie(movie_id=movie_id, title=title, duration=duration)
            else:
                print("Movies Not Found to Delete.")
        elif choice == "4":
            movies = fetch_all_movies()
            if len(movies) > 0:
                view_all_movies()
                movie_id = int(input("Enter movie ID to remove: "))
                delete_movie(movie_id)
            else:
                print("Movies Not Found for Delete.")
        elif choice == "5":
            break
        else:
            print("Bad choice!, Try Again")
