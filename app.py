import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Movie, Genre, Director, Actor, Writer
from forms import SignUpForm, LoginForm, EditForm
from utils import get_imdb_id, create_motion_picture
import requests

CURR_USER_KEY = "curr_user"

TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_API_KEY = '2c8276507ce2b6c8c6617c916d6fa4a1'
OMDB_BASE_URL = 'http://www.omdbapi.com'
OMDB_API_KEY = 'a2f9bc6'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///movieHub'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.before_request
def add_user_to_g():
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

@app.route('/')
def home():
    movies = Movie.query.all()
    if not g.user:
        return render_template('default_home.html', movies=movies)

    user = g.user
    return render_template('logged_home.html', user=user, movies=movies)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                image_url=form.image_url.data or User.image_url.default.arg
            )
            db.session.commit()

        except Exception:
            flash("Username taken")
            return render_template('signup.html', form=form)
        
        session[CURR_USER_KEY] = user.id
        return redirect('/')
    
    else:
        return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(username=form.username.data, password=form.password.data)

        if user:
            session[CURR_USER_KEY] = user.id
            return redirect('/')
        else:
            flash('Invalid username or password. Please try again')

    return render_template('login.html', form=form)

@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movie = Movie.query.get(movie_id)
    return render_template('details.html', movie=movie)

@app.route('/logout')
def logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    return redirect('/')

@app.route('/users/profile')
def profile():
    user = g.user
    return render_template('profile.html', user=user)

@app.route('/movies/genre/<int:genre_id>')
def genre_list(genre_id):
    movies_in_genre = requests.get(f'{TMDB_BASE_URL}/discover/movie', params={'api_key': TMDB_API_KEY, 'sort_by': 'popularity.dsc', 'with_genres': f'{genre_id}'}).json()

    movie_ids = [get_imdb_id(motion_picture['id']) 
                            for motion_picture in movies_in_genre['results']]
    for id in movie_ids:
        create_motion_picture(id)

    db.session.commit()
    movies = Movie.query.filter(Movie.genres == genre_id)

    return render_template('movie_categories.html', movies=movies)

@app.route('/users/edit', methods=['GET', 'POST'])
def edit_profile():
    user = g.user

    if not user:
        flash("access unauthorized.")
        return redirect('/')
    form = EditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.image_url = form.image_url.data

            db.session.commit()
            return redirect(f'/users/profile')
        flash('Incorrect password, please try again')
    
    return render_template('edit.html', form=form, user_id=user.id)

@app.route('/movies/add/watched/<int:movie_id>')
def add_to_watched(movie_id):
    user = g.user
    if not user:
        flash('You must be logged in to use this feature')
        return None

    movie = Movie.query.get(movie_id)
    user.movies_watched.append(movie)
    db.session.commit()
    return redirect(f'/movies/{movie_id}')

@app.route('/movies/add/favorites/<int:movie_id>')
def add_to_favorites(movie_id):
    user = g.user
    if not user:
        flash('You must be logged in to use this feature')
        return None

    movie = Movie.query.get(movie_id)
    user.favorite_movies.append(movie)
    db.session.commit()
    return redirect(f'/movies/{movie_id}')

@app.route('/movies/watched')
def watched():
    user = g.user
    if not user:
        flash('You must be logged in to use this feature')
        return None
    
    watched_movies = user.movies_watched
    return render_template('watched.html', user=user, movies=watched_movies)

@app.route('/movies/favorites')
def favorites():
    user = g.user
    if not user:
        flash('You must be logged in to use this feature')
        return None
    
    favorite_movies = user.favorite_movies
    return render_template('favorites.html', user=user, movies=favorite_movies)

@app.route('/movies/director/<int:director_id>')
def show_directors_movies(director_id):
    director = Director.query.get(director_id)
    directors_movies = director.movies

    return render_template('director_movies.html', director=director, movies=directors_movies)

@app.route('/movies/actor/<int:actor_id>')
def show_actors_movies(actor_id):
    actor = Actor.query.get(actor_id)
    actors_movies = actor.movies

    return render_template('actor_movies.html', actor=actor, movies=actors_movies)

@app.route('/movies/writer/<int:writer_id>')
def show_writers_movies(writer_id):
    writer = Writer.query.get(writer_id)
    writers_movies = writer.movies

    return render_template('writer_movies.html', writer=writer, movies=writers_movies)
