from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    movies_watched = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'))
    shows_watched = db.Column(db.Integer, db.ForeignKey('shows.id', ondelete='CASCADE'))
    watch_list_movies = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'))
    watch_list_shows = db.Column(db.Integer, db.ForeignKey('shows.id', ondelete='CASCADE'))
    favorite_movies = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'))
    favorite_shows = db.Column(db.Integer, db.ForeignKey('shows.id', ondelete='CASCADE'))

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class Director(db.Model):
    __tablename__ = 'directors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class Writer(db.Model):
    __tablename__ = 'writers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class ratingSource(db.Model):
    __tablename__ = 'rating_sources'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)



