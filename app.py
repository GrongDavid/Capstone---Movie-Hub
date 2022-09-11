import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Movie, Show
from forms import SignUpForm, LoginForm
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
def users_show(movie_id):
    movie = Movie.query.get(movie_id)
    return render_template('details.html', movie=movie)

@app.route('/logout')
def logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    return redirect('/')

@app.route('/profile')
def profile():
    user = g.user
    return render_template('profile.html', user=user)

@app.route('/movies/<movie_genre>')
def popular(movie_genre):
    existing_movies = Movie.query.all()
    TMDB_response = requests.get(f'{TMDB_BASE_URL}/{movie_genre}/movie/list', params={'api_key': TMDB_API_KEY}).json()
    motion_picture_ids = [get_imdb_id(motion_picture['id']) 
                            for motion_picture in TMDB_response['results']]

    for motion_picture_id in motion_picture_ids:
        new_motion_picture = create_motion_picture(motion_picture_id)
        for movie in existing_movies:
            if movie.title is not new_motion_picture.title:
                db.session.add(new_motion_picture)
        
    db.session.commit()
    genre_movies = Movie.query.filter(movie_genre=movie_genre)
    return render_template('movie_categories.html')

