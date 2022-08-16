import sqlite3, json

def get_data_from_db(query):
    """выполняет запрос к базе данных и возвращает список фильмов с указанием столбцов"""
    with sqlite3.connect("netflix.db") as con:
        con.row_factory = sqlite3.Row
        result = con.execute(query).fetchall()
        return result


def parse_to_dict(query):
    """
    :param query:
    :return: возвращает данные из DB в формате словаря
    """
    movies_data = get_data_from_db(query)
    result = []
    for movie in movies_data:
        result.append(dict(movie))
    return result


def get_movie_by_title(title) -> dict:
    """
    :param title: название фильма
    :return: возвращает фильм по названию
    """
    query = f''' 
                SELECT title, country, release_year, listed_in AS genre, description
                FROM netflix
                WHERE title='{title}'
                ORDER BY release_year DESC
                LIMIT 1'''

    return parse_to_dict(query)


def get_movies_by_years(start_year, end_year):
    """
    :param start_year: от какого года ищем
    :param end_year: до какого года ищем
    :return: список фильмав за указанный интервал
    """
    query = f"""
                SELECT title, release_year
                FROM netflix
                WHERE release_year BETWEEN {start_year} AND {end_year}
                LIMIT 100"""

    return parse_to_dict(query)


def get_movies_by_rating(category):
    """
    :param ratings: рейтинги фильмов
    :return: возвращает список фильмов по категории рейтингов
    """

    categories = {
        "children": ("G", "none"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }

    ratings = categories.get(category)

    query = f"""
                SELECT title, rating, description
                FROM netflix
                WHERE rating IN {ratings}
                LIMIT 100"""

    return parse_to_dict(query)


def get_movies_by_genre(genre):
    """
    :param genre: жанр фильмов
    :return: возвращает самые свежие 10 фильмов по жанру
    """
    query = f"""
                SELECT title, description
                FROM netflix
                WHERE listed_in like "%{genre}%"
                ORDER BY release_year DESC 
                LIMIT 10
                """

    return parse_to_dict(query)


def get_frequent_actors(actor_one, actor_two):
    """
    :param actor_one:
    :param actor_two:
    :return: Возвращает список актеров, которые играли с заданными двумя актерами больше 2х раз
    """
    query = f"""
                SELECT "cast"
                FROM netflix
                WHERE "cast" LIKE "%{actor_one}%"
                AND "cast" LIKE "%{actor_two}%"
                """

    movies = parse_to_dict(query)
    actors_heap = []

    # собираем список всех актеров из всех фильмов
    for movie in movies:
        cast = movie.get("cast", "")
        actors_heap.extend([actor.strip() for actor in cast.split(",")])

    unique_actors = set(actors_heap) - set([actor_one, actor_two])

    # проверяем, что актер встречается в сборном списке актеров больше 2х раз
    return [actor for actor in unique_actors if actors_heap.count(actor) > 2]


def get_movie_by_year_type_genre(year, movie_type, genre):
    """
    :param year: год картины
    :param movie_type: тип картины(Movie/TV Show)
    :param genre: жанр
    :return: возвращает список картин в формате JSON по заданным параметрам
    """

    query = f"""
                SELECT release_year, description
                FROM netflix
                WHERE release_year={year}
                AND type="{movie_type}"
                AND listed_in LIKE "%{genre}%"
                """

    movies = parse_to_dict(query)
    return json.dumps(movies)

print(get_movie_by_year_type_genre(2000, "Movie", "Drama"))