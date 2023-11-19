from typing import List

from models.movie_model import MovieModel
from datetime import datetime
import json
import inquirer

MOVIE_FILE = 'Movies.dat'


def fetch_all_movies():
    try:
        with open(MOVIE_FILE, 'r') as f:
            movies_data = json.load(f)
        return [MovieModel.deserialize(movie) for movie in movies_data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_all_movies(movies: List[MovieModel]):
    with open(MOVIE_FILE, 'w') as f:
        json.dump([movie.serialize() for movie in movies] or [], f)


def view_all_movies():
    movies = fetch_all_movies()
    if not movies:
        print("No Movies")
        return

    headers = ["ID", "Movie Title", "Duration", "Rating"]
    column_widths = [max(len(header), max((len(str(getattr(movie, attr))) for movie in movies), default=0)) for
                     header, attr in zip(headers, ['movie_id', 'title', 'duration', 'rating'])]

    header_row = " | ".join(header.ljust(width) for header, width in zip(headers, column_widths))
    print(header_row)
    print("-" * len(header_row))

    for movie in movies:
        movie_details = [
            str(movie.movie_id),
            movie.title,
            f"{movie.duration} min",
            f"{movie.rating if movie.rating is not None else 'N/A'}"
        ]
        row = " | ".join(detail.ljust(width) for detail, width in zip(movie_details, column_widths))
        print(row)


def show_movie_details_by_name(movie_title):
    movies = fetch_all_movies()

    movie = next((mv for mv in movies if mv.title.lower() == movie_title.lower()), None)
    if not movie:
        print(f"No movie found with title '{movie_title}'")
        return

    movie_data = {
        "Movie ID": movie.movie_id,
        "Title": movie.title,
        "Duration": f"{movie.duration} min",

    }
    headers = movie_data.keys()
    column_widths = {header: max(len(header), len(str(movie_data[header]))) for header in headers}

    header_row = " | ".join(header.ljust(column_widths[header]) for header in headers)
    print(header_row)
    print("-" * len(header_row))

    row = " | ".join(str(movie_data[header]).ljust(column_widths[header]) for header in headers)
    print(row)


def select_movie():
    movies = fetch_all_movies()

    if not movies:
        print("No movies found.")
        return None

    movie_choices = [(f"{movie.title} ({movie.duration} minutes)", movie.movie_id) for movie in movies]

    question = [
        inquirer.List('movie',
                      message="Select a movie:",
                      choices=movie_choices,
                      carousel=True)
    ]

    answers = inquirer.prompt(question)

    selected_movie_id = answers['movie']
    return next((movie for movie in movies if movie.movie_id == selected_movie_id), None)


def get_movie_id_using_interactive_console():
    movies = fetch_all_movies()
    movie_choices = [(movie.title, movie.movie_id) for movie in movies]

    movie_question = [
        inquirer.List('movie',
                      message="Select Movie",
                      choices=movie_choices,
                      carousel=True)
    ]
    selected_movie_id = inquirer.prompt(movie_question)['movie']
    return selected_movie_id


def convert_showing_time(time_str):
    for fmt in ("%I:%M %p", "%H:%M"):
        try:
            return datetime.strptime(time_str, fmt).time()
        except ValueError:
            print(f"Time '{time_str}' is not in a valid format.")
            pass
    raise ValueError(f"Time '{time_str}' is not in a valid format.")


def convert_str_to_time(time_str):
    # Define the format for the time string
    time_format = "%I:%M %p"  # or "%I:%M %p" for 12-hour format with AM/PM
    try:
        return datetime.strptime(time_str, time_format).time()
    except ValueError:
        print(f"Time '{time_str}' is not in the valid format.")
        return None


def add_movie(title, duration):
    movies = fetch_all_movies()
    movie_id = max(movie.movie_id for movie in movies) + 1 if movies else 1
    new_movie = MovieModel(movie_id=movie_id, title=title, duration=duration)
    movies.append(new_movie)
    save_all_movies(movies)
    print("Movie Added!")


def delete_movie(movie_id):
    movies = fetch_all_movies()
    movies = [movie for movie in movies if movie.movie_id != movie_id]
    save_all_movies(movies)
    view_all_movies()


def update_movie(movie_id, title=None, duration=None, rating=None):
    movies = fetch_all_movies()
    updated = False

    for movie in movies:
        if movie.movie_id == movie_id:
            if title != "":
                movie.title = title
            if duration != "":
                movie.duration = duration
            if rating != "":
                movie.rating = rating
            updated = True
            break

    if updated:
        save_all_movies(movies)
        print(f"Movie having ID {movie_id} has been updated successfully.")
    else:
        print(f"Movie having ID {movie_id} not found.")


def get_movie_using_id(movie_id):
    all_movies = fetch_all_movies()
    return next((movie for movie in all_movies if movie.movie_id == movie_id), None)


def format_show_time_for_display(show_time):
    return show_time.strftime("%I:%M %p")
