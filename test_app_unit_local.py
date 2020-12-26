#########################################################################
#
# @file name: test_app_unit_local.py
# @purpose: test file of backend app on local instance. Although permissions
# are tested in this file, the focus is on each possible endpoint error.
# conversely, test_app_hosted.py thoroughly tests permissions accessing 
# the deployed instance on heroku and associated postgres database.
# @author: Tony Burge
# @date: 2020-09-09
#
#########################################################################
#
# global imports
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
#
# local imports
from app import create_app
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth
from test_config import jwt_ep, jwt_cd, jwt_ca, jwt_no, ACCTS
from test_config import movie1, movie2, movie3, actor1, actor2
from test_config import umovie1, umovie2, umovie3, uactor1, uactor2


# test case class for casting app
class CastingTestCase(unittest.TestCase):
    #
    # set up test environment
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)
        #
        # bind app to current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    # executed after each test
    def tearDown(self):
        pass

    # ----------------------------------------------------------------------
    # POST tests
    # ----------------------------------------------------------------------

    # ACTORS
    #
    # unauthorized: add actor (casting assistant)
    def test_401_add_actor(self):
        test = (self.client().post('/actors', json=actor1,
                headers={"Authorization": "Bearer {}".format(jwt_ca)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 401)

    # authorized: add actor (casting director)
    def test_200_add_actor(self):
        test = (self.client().post('/actors', json=actor1,
                headers={"Authorization": "Bearer {}".format(jwt_cd)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_id'])

    # authorized: add actor but missing required fields
    def test_412_add_actor_missing_fields(self):
        test = (self.client().post('/actors', json=actor2,
                headers={"Authorization": "Bearer {}".format(jwt_cd)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 412)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],
                         'precondition failed or request data missing')

    # MOVIES
    #
    # unauthorized: add movie (casting director)
    def test_401_add_movie(self):
        test = (self.client().post('/movies', json=movie1,
                headers={"Authorization": "Bearer {}".format(jwt_cd)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 401)

    # authorized: add movie (executive producer)
    def test_200_add_movie(self):
        test = (self.client().post('/movies', json=movie1,
                headers={"Authorization": "Bearer {}".format(jwt_ep)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie_id'])

    # authorized: add movie but missing cast list
    def test_412_add_movie_no_cast(self):
        test = (self.client().post('/movies', json=movie2,
                headers={"Authorization": "Bearer {}".format(jwt_ep)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 412)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],
                         'precondition failed or request data missing')

    # authorized: add movie but missing required fields
    def test_412_add_movie_missing_fields(self):
        test = (self.client().post('/movies', json=movie3,
                headers={"Authorization": "Bearer {}".format(jwt_ep)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 412)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],
                         'precondition failed or request data missing')

    # ----------------------------------------------------------------------
    # PATCH tests
    # ----------------------------------------------------------------------

    # ACTORS
    #
    # unauthorized: update actor (casting assistant)
    def test_401_update_actor(self):
        test = (self.client().patch('/actors/2', json=uactor1,
                headers={"Authorization": "Bearer {}".format(jwt_ca)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 401)

    # authorized: update actor (casting director)
    def test_200_update_actor(self):
        test = (self.client().patch('/actors/2', json=uactor1,
                headers={"Authorization": "Bearer {}".format(jwt_cd)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 200)
        self.assertEqual(data['success'], True)

    # authorized: update actor (casting director), but wrong id
    def test_412_update_actor_unknown_id(self):
        test = (self.client().patch('/actors/-1', json=uactor1,
                headers={"Authorization": "Bearer {}".format(jwt_cd)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 412)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],
                         'precondition failed or request data missing')

    # authorized: update actor (casting director), but no recognized fields
    def test_412_update_actor_no_fields(self):
        test = (self.client().patch('/actors/2', json=uactor2,
                headers={"Authorization": "Bearer {}".format(jwt_cd)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 412)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],
                         'precondition failed or request data missing')

    # MOVIES
    #
    # unauthorized: update movie (casting assistant)
    def test_401_update_movie(self):
        test = (self.client().patch('/movies/2', json=umovie1,
                headers={"Authorization": "Bearer {}".format(jwt_ca)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 401)

    # authorized: update movie (casting director)
    def test_200_update_movie(self):
        test = (self.client().patch('/movies/2', json=umovie1,
                headers={"Authorization": "Bearer {}".format(jwt_cd)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 200)
        self.assertEqual(data['success'], True)

    # authorized: update movie (casting director), but wrong id
    def test_412_update_movie_unknown_id(self):
        test = (self.client().patch('/movies/-1', json=umovie1,
                headers={"Authorization": "Bearer {}".format(jwt_cd)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 412)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],
                         'precondition failed or request data missing')

    # authorized: update movie (casting director), but no regognized fields
    def test_412_update_movie_no_fields(self):
        test = (self.client().patch('/movies/2', json=umovie2,
                headers={"Authorization": "Bearer {}".format(jwt_cd)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 412)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],
                         'precondition failed or request data missing')

    # authorized: update movie (casting director), but empty cast list
    def test_412_update_movie_empty_castlist(self):
        test = (self.client().patch('/movies/2', json=umovie3,
                headers={"Authorization": "Bearer {}".format(jwt_cd)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 412)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],
                         'precondition failed or request data missing')

    # ----------------------------------------------------------------------
    # GET tests
    # ----------------------------------------------------------------------

    # ACTORS
    #
    # unauthorized: get actors (public)
    def test_401_get_actors(self):
        test = (self.client().get('/actors',
                headers={"Authorization": "Bearer {}".format(jwt_no)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 401)

    # authorized: get movies (casting assistant)
    def test_200_get_actors(self):
        test = (self.client().get('/actors',
                headers={"Authorization": "Bearer {}".format(jwt_ca)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # MOVIES
    #
    # unauthorized: get movies (public)
    def test_401_get_movies(self):
        test = (self.client().get('/movies',
                headers={"Authorization": "Bearer {}".format(jwt_no)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 401)

    # authorized: get movies (casting assistant)
    def test_200_get_movies(self):
        test = (self.client().get('/movies',
                headers={"Authorization": "Bearer {}".format(jwt_ca)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # ----------------------------------------------------------------------
    # DELETE tests
    # ----------------------------------------------------------------------

    # ACTORS
    #
    # unauthorized: delete actor (casting assistant)
    def test_401_delete_actor(self):
        test = (self.client().delete('/actors/1',
                headers={"Authorization": "Bearer {}".format(jwt_ca)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 401)

    # authorized: delete actor (casting director)
    def test_200_delete_actor(self):
        test = (self.client().delete('/actors/1',
                headers={"Authorization": "Bearer {}".format(jwt_cd)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 200)
        self.assertEqual(data['success'], True)

    # authorized: delete actor but unknown actor_id
    def test_412_delete_actor_unknown_id(self):
        test = (self.client().delete('/actors/-1',
                headers={"Authorization": "Bearer {}".format(jwt_cd)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 412)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],
                         'precondition failed or request data missing')

    # MOVIES
    #
    # unauthorized: delete movie (casting director)
    def test_401_delete_movie(self):
        test = (self.client().delete('/movies/1',
                headers={"Authorization": "Bearer {}".format(jwt_cd)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 401)

    # authorized: delete movie (executive producer)
    def test_200_delete_movie(self):
        test = (self.client().delete('/movies/1',
                headers={"Authorization": "Bearer {}".format(jwt_ep)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 200)
        self.assertEqual(data['success'], True)

    # authorized: delete movie but unknown movie_id
    def test_412_delete_movie_unknown_id(self):
        test = (self.client().delete('/movies/-1',
                headers={"Authorization": "Bearer {}".format(jwt_ep)}))
        data = json.loads(test.data)
        self.assertEqual(test.status_code, 412)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],
                         'precondition failed or request data missing')


#
# Main: run app
if __name__ == "__main__":
    unittest.main()
