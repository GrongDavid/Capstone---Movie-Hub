from app import db
from models import User, Movie, Genre, Actor
import requests
import pdb

TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_API_KEY = '2c8276507ce2b6c8c6617c916d6fa4a1'
OMDB_BASE_URL = 'http://www.omdbapi.com'
OMDB_API_KEY = 'a2f9bc6'


def get_imdb_id(TMDB_id):
    imdb_id = requests.get(
        f'{TMDB_BASE_URL}/movie/{TMDB_id}',
        params={'api_key': TMDB_API_KEY}
    ).json()['imdb_id']

    return imdb_id

def get_movie(imdb_id):
    movie = requests.get(
        OMDB_BASE_URL,
        params={'apikey': OMDB_API_KEY, 'i': imdb_id, 'plot': 'full'}
    ).json()

    return movie

def create_motion_picture(id):
    all_genres = Genre.query.all()
    title = get_movie(id)['Title']
    plot = get_movie(id)['Plot']
    release_date = get_movie(id)['Released']
    runtime = get_movie(id)['Runtime'].split()[0]
    if runtime == 'N/A':
        runtime = -1
    else:
        try:
            runtime = int(runtime)
        except Exception:
            runtime = -1
    genre_names = get_movie(id)['Genre'].split()
    directors = get_movie(id)['Director'].split()
    writers = get_movie(id)['Writer'].split()
    actors = get_movie(id)['Actors']
    poster = get_movie(id)['Poster']
    # rating_sources = [get_movie(id)['Ratings']
    #                     for source in ]
    new_movie = Movie(title=title, plot=plot, release_date=release_date, runtime=runtime, poster=poster)
    for name in genre_names:
        for genre in all_genres:
            if name == genre.name:
                new_movie.genres.append(genre)
            elif name + ',' == genre.name:
                new_movie.genres.append(genre)
    print(new_movie.genres)

    db.session.add(new_movie)
