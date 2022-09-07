from app import db
from models import User, Movie, Show, Genre, Actor
import requests

TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_API_KEY = '2c8276507ce2b6c8c6617c916d6fa4a1'
OMDB_BASE_URL = 'http://www.omdbapi.com'
OMDB_API_KEY = 'a2f9bc6'

TMDB_popular_response = requests.get(f'{TMDB_BASE_URL}/movie/popular', params={'api_key': TMDB_API_KEY}).json()

def get_imdb_id(TMDB_movie_id):
    imdb_id = requests.get(
        f'{TMDB_BASE_URL}/movie/{TMDB_movie_id}',
        params={'api_key': TMDB_API_KEY}
    ).json()['imdb_id']

    return imdb_id

def get_movie(imdb_id):
    movie = requests.get(
        OMDB_BASE_URL,
        params={'apikey': OMDB_API_KEY, 'i': imdb_id}
    ).json()

    return movie

motion_picture_id_list = [get_imdb_id(motion_picture['id']) 
                            for motion_picture in TMDB_popular_response['results']]

  
db.drop_all()
db.create_all()

for movie_id in motion_picture_id_list:
    print(get_movie(movie_id)['Title'])
    title = get_movie(movie_id)['Title']
    release_date = get_movie(movie_id)['Released']
    runtime = get_movie(movie_id)['Runtime']
    # if runtime == 'N/A':
    #     runtime = -1
    # else:
        # runtime = int(runtime)
    genres = get_movie(movie_id)['Genre'].split()
    directors = get_movie(movie_id)['Director'].split()
    writers = get_movie(movie_id)['Writer'].split()
    actors = get_movie(movie_id)['Actors']
    poster = get_movie(movie_id)['Poster']
    # rating_sources = [get_movie(movie_id)['Ratings']
    #                     for source in ]
    # if runtime < 59:
    #     new_show = Show(title=title, release_date=release_date, runtime=runtime)
    #     db.session.add(new_show)
    new_movie = Movie(title=title, release_date=release_date, runtime=runtime, poster=poster)
    db.session.add(new_movie)

db.session.commit()
100


