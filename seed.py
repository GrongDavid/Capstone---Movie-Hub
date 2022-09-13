from app import db
from models import User, Movie, Genre, Actor
from utils import get_imdb_id, create_motion_picture
import requests

TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_API_KEY = '2c8276507ce2b6c8c6617c916d6fa4a1'
OMDB_BASE_URL = 'http://www.omdbapi.com'
OMDB_API_KEY = 'a2f9bc6'

TMDB_popular_response = requests.get(f'{TMDB_BASE_URL}/movie/popular', params={'api_key': TMDB_API_KEY}).json()

movie_ids = [get_imdb_id(motion_picture['id']) 
                            for motion_picture in TMDB_popular_response['results']]
all_genres = requests.get(f'{TMDB_BASE_URL}/genre/movie/list', params={'api_key': TMDB_API_KEY}).json()

  
db.drop_all()
db.create_all()

for genre in all_genres['genres']:
    name = genre['name']
    genre_id = genre['id']
    new_genre = Genre(name=name, genre_id=genre_id)
    db.session.add(new_genre)

for id in movie_ids:
    create_motion_picture(id)

db.session.commit()


