import os
from unittest import TestCase

from models import db, connect_db, User, Movie

os.environ['DATABASE_URL'] = "postgresql:///movieHub-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class ViewTestCase(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username='test', password='abc123', image_url=None)
        self.testuser.id = 1

        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        return super().tearDown()

    def test_home(self):
        movie1 = Movie(title='test', release_date='test_date', runtime='105', 
                        plot='A test movie that tests', earnings=104)
        movie1.id = 1
        db.session.add(movie1)
        db.session.commit()

        movie = Movie.query.get(1)
        with self.client as c:
            response = c.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)

            self.assertIn(f'<img src="{movie.poster}"', html)

    def test_details(self):
        movie2 = Movie(title='test2', release_date='test_date', runtime='85', 
                        plot='Another test movie that tests', earnings=205)
        movie2.id = 2
        db.session.add(movie2)
        db.session.commit()

        movie = Movie.query.get(2)
        with self.client as c:
            response = c.get('/movies/2')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)

            self.assertIn(f'<p><b>Earnings: </b>{movie.earnings}</p>', html)
            self.assertIn(f'<p><b>IMDB Rating: </b>{movie.imdb_rating}</p>', html)
            self.assertIn(f'<h5><b>Plot Details: </b>{movie.plot}</h5>', html)
            self.assertIn(f'<img src="{movie.poster}"', html)
            self.assertIn(f'<p><b>Runtime: </b>{movie.runtime} min</p>', html)

    def test_watchlist(self):
        movie3 = Movie(title='test3', release_date='test_date', runtime='85', 
                        plot='Another test movie that tests', earnings=205)
        movie3.id = 3
        db.session.add(movie3)
        db.session.commit()

        user = User.query.get(1)
        
        # Ensure watched movies is correctly 0 before checking if it appended correctly
        self.assertEqual(len(user.movies_watched), 0)
        user.movies_watched.append(movie3)
        self.assertEqual(len(user.movies_watched), 1)

    def test_favorite_list(self):
        movie4 = Movie(title='test4', release_date='test_date', runtime='85', 
                        plot='Another test movie that tests', earnings=205)
        movie4.id = 4
        db.session.add(movie4)
        db.session.commit()

        user = User.query.get(1)
        
        # Ensure favorite movies is correctly 0 before checking if it appended correctly
        self.assertEqual(len(user.favorite_movies), 0)
        user.favorite_movies.append(movie4)
        self.assertEqual(len(user.favorite_movies), 1)


