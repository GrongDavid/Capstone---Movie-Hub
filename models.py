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
    # movies_watched_id = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'))
    # favorite_movie_id = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'))
    
    movies_watched = db.relationship('Movie', secondary='users_watched_movies', backref='users_watched')
    favorite_movies = db.relationship('Movie', secondary='users_favorited_movies', backref='users_favorited')

    
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
    plot = db.Column(db.Text)
    awards = db.Column(db.Text)
    poster = db.Column(db.Text, nullable=False, default='https://img.myloview.com/posters/letter-n-a-icon-logo-design-concept-400-168449363.jpg')
    rating = db.Column(db.Text)
    earnings = db.Column(db.Integer)

    genres = db.relationship('Genre', secondary='movies_genres', backref='movies')
    directors = db.relationship('Director', secondary='movies_directors', backref='movies')
    writers = db.relationship('Writer', secondary='movies_writers', backref='movies')
    actors = db.relationship('Actor', secondary='movies_actors', backref='movies')
    # rating_sources = db.relationship('ratingSource', backref='movies')
    

class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    genre_id = db.Column(db.Text)

class Director(db.Model):
    __tablename__ = 'directors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))

class Writer(db.Model):
    __tablename__ = 'writers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))

class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    movie_ids = db.Column(db.Integer, db.ForeignKey('movies.id'))

class ratingSource(db.Model):
    __tablename__ = 'rating_sources'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)

class MovieGenre(db.Model):
    __tablename__ = 'movies_genres'

    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), primary_key=True)

class UserWatchMovie(db.Model):
    __tablename__ = 'users_watched_movies'

    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

class UserFavoriteMovie(db.Model):
    __tablename__ = 'users_favorited_movies'

    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

class MovieDirector(db.Model):
    __tablename__ = 'movies_directors'

    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'), primary_key=True)

class MovieActor(db.Model):
    __tablename__ = 'movies_actors'

    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), primary_key=True)

class MovieWriter(db.Model):
    __tablename__ = 'movies_writers'

    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    writer_id = db.Column(db.Integer, db.ForeignKey('writers.id'), primary_key=True)



