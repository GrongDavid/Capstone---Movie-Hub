from app import db
from models import User, Movie, Genre, Actor, Director, Writer
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

def add_directors(director_list, movie):
    for director in director_list:
        try:
            new_director = Director(name=director)
            db.session.add(new_director)
            db.session.commit()

            movie.directors.append(new_director)
        except Exception:
            db.session.rollback()
            continue
    return None

def add_actors(actor_list, movie):
    for actor in actor_list:
        try:
            new_actor = Actor(name=actor)
            db.session.add(new_actor)
            db.session.commit()

            movie.actors.append(new_actor)
        except Exception:
            db.session.rollback()
            continue
    return None

def add_writers(writer_list, movie):
    for writer in writer_list:
        try:
            new_writer = Writer(name=writer)
            db.session.add(new_writer)
            db.session.commit()

            movie.writers.append(new_writer)
        except Exception:
            db.session.rollback()
            continue
    return None

def create_motion_picture(id):
    all_genres = Genre.query.all()
    title = get_movie(id)['Title']
    plot = get_movie(id)['Plot']
    release_date = get_movie(id)['Released']
    runtime = get_movie(id)['Runtime'].split()[0]
    genre_names = get_movie(id)['Genre'].split()
    directors = set(get_movie(id)['Director'].split(','))
    writers = set(get_movie(id)['Writer'].split(','))
    actors = set(get_movie(id)['Actors'].split(','))
    poster = get_movie(id)['Poster']

    if runtime == 'N/A':
        runtime = -1
    else:
        try:
            runtime = int(runtime)
        except Exception:
            runtime = -1

    new_movie = Movie(title=title, plot=plot, release_date=release_date, runtime=runtime, poster=poster)
    for name in genre_names:
        for genre in all_genres:
            if name == genre.name:
                new_movie.genres.append(genre)
            elif name + ',' == genre.name:
                new_movie.genres.append(genre)
    
    add_directors(directors, new_movie)
    add_actors(actors, new_movie)
    add_writers(writers, new_movie)

    db.session.add(new_movie)


