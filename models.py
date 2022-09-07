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
    image_url = db.Column(db.Text, default='https://t3.ftcdn.net/jpg/03/46/83/96/360_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg')
    movies_watched = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'))
    shows_watched = db.Column(db.Integer, db.ForeignKey('shows.id', ondelete='CASCADE'))
    watch_list_movies = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'))
    watch_list_shows = db.Column(db.Integer, db.ForeignKey('shows.id', ondelete='CASCADE'))
    favorite_movies = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'))
    favorite_shows = db.Column(db.Integer, db.ForeignKey('shows.id', ondelete='CASCADE'))

    @classmethod
    def signup(cls, username, password, image_url):
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()

        if user:
            valid = bcrypt.check_password_hash(user.password, password)
            if valid:
                return user
        return False

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    release_date = db.Column(db.Text)
    runtime = db.Column(db.Text)
    # genres = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=False)
    # directors = db.Column(db.Integer, db.ForeignKey('directors.id'), nullable=False)
    # writers = db.Column(db.Integer, db.ForeignKey('writers.id'))
    # actors = db.Column(db.Integer, db.ForeignKey('actors.id'))
    # rating_source = db.Column(db.Integer, db.ForeignKey('rating_sources.id'))
    plot = db.Column(db.Text)
    awards = db.Column(db.Text)
    poster = db.Column(db.Text, nullable=False, default='https://img.myloview.com/posters/letter-n-a-icon-logo-design-concept-400-168449363.jpg')
    rating = db.Column(db.Text)
    earnings = db.Column(db.Integer)
    
class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    release_date = db.Column(db.Text)
    runtime = db.Column(db.Integer)
    # genres = db.Column(db.Integer, db.ForeignKey('genres.id', ondelete='CASCADE'), nullable=False)
    # directors = db.Column(db.Integer, db.ForeignKey('directors.id', ondelete='CASCADE'), nullable=False)
    # writers = db.Column(db.Integer, db.ForeignKey('writers.id', ondelete='CASCADE'))
    # rating_source = db.Column(db.Integer, db.ForeignKey('rating_sources.id', ondelete='CASCADE'))
    plot = db.Column(db.Text)
    awards = db.Column(db.Text)
    poster = db.Column(db.Text, nullable=False, default='https://img.myloview.com/posters/letter-n-a-icon-logo-design-concept-400-168449363.jpg')
    rating = db.Column(db.Text)
    earnings = db.Column(db.Integer)

class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    movie_ids = db.Column(db.Integer, db.ForeignKey('movies.id'))
    show_ids = db.Column(db.Integer, db.ForeignKey('shows.id'))

class Director(db.Model):
    __tablename__ = 'directors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    movie_ids = db.Column(db.Integer, db.ForeignKey('movies.id'))
    show_ids = db.Column(db.Integer, db.ForeignKey('shows.id'))

class Writer(db.Model):
    __tablename__ = 'writers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    movie_ids = db.Column(db.Integer, db.ForeignKey('movies.id'))
    show_ids = db.Column(db.Integer, db.ForeignKey('shows.id'))

class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    movie_ids = db.Column(db.Integer, db.ForeignKey('movies.id'))
    show_ids = db.Column(db.Integer, db.ForeignKey('shows.id'))

class ratingSource(db.Model):
    __tablename__ = 'rating_sources'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)



