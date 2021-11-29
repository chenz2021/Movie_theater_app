import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import db_setup, Movie, Theater, Showtime, db_drop_and_create_all


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.user = "postgres"
        self.password = "1"
        self.database_name = "theater_test"
        self.database_path = "postgresql://{}:{}@{}/{}". \
            format(self.user, self.password, 'localhost:5432', self.database_name)

        self.movie = {
            'title': 'Titanic',
            'image_link': 'https://www.imdb.com/title/tt0120338/mediaviewer/rm2647458304/',
            'trailer': 'https://www.imdb.com/video/vi907189785?playlistId=tt0120338&ref_=tt_pr_ov_vi',
            'review': 'https://www.imdb.com/title/tt0120338/',
            'description': 'Greatest love film ever!'
        }
        self.theater = {
            'name': 'AMC',
            'city': 'Boston',
            'state': 'MA',
            'address': 'some Rd',
            'phone': 'some number',
            'website': 'some website'
        }
        self.theater_patch = {
            'name': 'need to update'
        }
        db_setup(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_movie(self):
        res = self.client().post('/movies', json=self.movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def get_movie_by_id(self):
        res = self.client().get('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def get_movie_by_invalid_id(self):
        res = self.client().get('/movies/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def delete_movie_by_id(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'])

    def delete_movie_by_invalid_id(self):
        res = self.client().delete('/movies/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_movie_search_with_results(self):
        res = self.client().post("/movies/search", json={"search_term": "Titanic"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['response'])

    def test_movie_search_with_no_results(self):
        res = self.client().post("/movies/search", json={'search_term': '111'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data['response']['count'], 0)

    def test_get_theaters(self):
        res = self.client().get('/theaters')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie_info'])

    def test_get_theater_with_theater_id(self):
        res = self.client().get('/theaters/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['showtime_info'])

    def test_get_theater_with_invalid_theater_id(self):
        res = self.client().get('/theaters/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    def test_post_theater(self):
        res = self.client().post("/theaters", json=self.theater)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def delete_theater_by_id(self):
        res = self.client().delete('/theaters/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'])

    def delete_theater_by_invalid_id(self):
        res = self.client().delete('/theaters/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_patch_theater_by_id(self):
        res = self.client().patch('/theaters/1', json=self.theater_patch)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
