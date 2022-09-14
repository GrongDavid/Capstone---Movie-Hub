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
    
    movies_watched = db.relationship('Movie', backref='users_watched')
    favorite_movies = db.relationship('Movie', backref='users_favorited')

    
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    genres = db.relationship('Genre', secondary='movies_genres', backref='movies')
    directors = db.relationship('Director', backref='movies')
    writers = db.relationship('Writer', backref='movies')
    actors = db.relationship('Actor', backref='movies')
    # rating_sources = db.relationship('ratingSource', backref='movies')
    

class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    genre_id = db.Column(db.Text)

class MovieGenre(db.Model):
    __tablename__ = 'movies_genres'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    
class Director(db.Model):
    __tablename__ = 'directors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    movie_ids = db.Column(db.Integer, db.ForeignKey('movies.id'))

class Writer(db.Model):
    __tablename__ = 'writers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    movie_ids = db.Column(db.Integer, db.ForeignKey('movies.id'))

class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    movie_ids = db.Column(db.Integer, db.ForeignKey('movies.id'))

class ratingSource(db.Model):
    __tablename__ = 'rating_sources'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)



