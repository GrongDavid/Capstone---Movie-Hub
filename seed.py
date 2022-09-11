from app import db
from models import User, Movie, Show, Genre, Actor
from utils import get_imdb_id, create_motion_picture
import requests

TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_API_KEY = '2c8276507ce2b6c8c6617c916d6fa4a1'
OMDB_BASE_URL = 'http://www.omdbapi.com'
OMDB_API_KEY = 'a2f9bc6'

TMDB_popular_response = requests.get(f'{TMDB_BASE_URL}/movie/popular', params={'api_key': TMDB_API_KEY}).json()

motion_picture_ids = [get_imdb_id(motion_picture['id']) 
                            for motion_picture in TMDB_popular_response['results']]

  
db.drop_all()
db.create_all()

create_motion_picture(motion_picture_ids)

db.session.commit()


