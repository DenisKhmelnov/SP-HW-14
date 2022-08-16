from flask import Flask, jsonify
from utils import get_movie_by_title, get_movies_by_years, get_movies_by_rating, get_movies_by_genre

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_AS_ASCII'] = False


@app.get('/movie/<title>')
def movie_by_title(title):  # put application's code here
    movie = get_movie_by_title(title)
    return jsonify(movie[0])


@app.get('/movie/<int:start_year>/to/<int:end_year>')
def movies_by_years(start_year, end_year):
    movies = get_movies_by_years(start_year, end_year)
    return movies


@app.get('/rating/<category>')
def movies_by_rating(category):
    movies = get_movies_by_rating(category)
    return movies


@app.get('/genre/<genre>')
def movies_by_genre(genre):
    movies = get_movies_by_genre(genre)
    return movies


if __name__ == '__main__':
    app.run()
