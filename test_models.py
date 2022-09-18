import os
from unittest import TestCase
from models import db, User, Movie, Genre, Actor, Director, Writer

os.environ['DATABASE_URL'] = "postgresql:///movieHub-test"

from app import app

db.create_all()

class ModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()
        Movie.query.delete()

        user1 = User.signup('user1', 'abc123')
        user1.id = 1
        db.session.commit()

        u1 = User.query.get(1)
        self.u1 = u1

        self.client = app.test_client()

    def tearDown(self):
        down = super().tearDown()
        db.session.rollback()
        return down

    def test_user_model(self):
        user = User(username='testuser', password='abc123')
        db.session.add(user)
        db.session.commit()
        
        # User should have no watched or favorited movies
        self.assertEqual(len(user.movies_watched), 0)
        self.assertEqual(len(user.favorite_movies), 0)

    def test_signup(self):
        user = User(username='testuser', password='abc123')
        user.id = 2
        db.session.commit()

        user = User.query.get(2)

        self.assertEqual(user.username, 'testuser')

        # If equal, password was not hashed correctly
        self.assertNotEqual(user.password, 'abc123')

    def test_auth(self):
        user = User.authenticate(self.u1.username, 'abc123')
        self.assertEqual(user.id, self.u1.id)

    def test_movie(self):
        movie1 = Movie(title='test', release_date='test_date', runtime='105', 
                        plot='A test movie that tests', earnings='104mil')
        movie1.id = 1
        db.session.add(movie1)
        db.session.commit()

        movie = Movie.get(1)

    def test_genre(self):
        pass

    def test_director(self):
        pass

    def test_actor(self):
        pass

    def test_writer(self):
        pass



