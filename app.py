#########################################################################
#
# @file name: app.py
# @purpose: main file of backend app
# @author: Tony Burge
# @date: 2020-09-08
#
#########################################################################
#
# global imports
import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
#
# local imports
from models import db, setup_db, Movie, Actor
from auth import AuthError, requires_auth

#########################################################################
# main app creation
#########################################################################
#
def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    # instantiate CORS and add after_request decorator and CORS headers
    cors = CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        #
        return response

    #####################################################################
    # route handlers
    #####################################################################

    # --------------------------------------------------------------------
    # GET handlers
    # --------------------------------------------------------------------

    # get list of movies route handler
    # empty list is acceptable if no movies have been added
    # list to be sorted in ascending order by title
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(jwt):
        movie_list = []
        movies = Movie.query.order_by(Movie.title).all()
        for movie in movies:
            # get list of actors in this movie
            actor_list = [actor.create_dict() for actor in movie.castmembers]
            # append movie entry to movie_list
            movie_list.append({
                "id": movie.id,
                "title": movie.title,
                "release_date": movie.release_date,
                "actors": actor_list
            })
        return jsonify({
            'success': True,
            'movies': movie_list
        })

    # get list of actors route handler
    # empty list is acceptable if no actors have been added
    # list to be sorted in ascending order by actor name
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(jwt):
        #
        actors = Actor.query.order_by(Actor.name).all()
        actor_list = [actor.create_dict() for actor in actors]
        return jsonify({
            'success': True,
            'actors': actor_list
        })

    # --------------------------------------------------------------------
    # POST handlers
    # --------------------------------------------------------------------

    # add movie route handler
    # if all fields are not presented by json, abort 412
    # if cast list is empty, abort 412 (movie must have at least one actor)
    # note: cast list should only contain id of actors, for example:
    # cast = [1, 3]
    # if cast list includes non-existent ids, abort 412
    # otherwise attempt to add new movie to database
    # if not successful, abort 422
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(jwt):
        json_input = request.get_json()
        title = json_input.get('title')
        release_date = json_input.get('release_date')
        cast_list = json_input.get('cast')
        #
        # if any fields are blank, abor 412 (even though
        # from end should catch this, I don't want to assume
        # that is the case)
        if (title is None or release_date is None or cast_list is None):
            abort(412)
        #
        # if cast list exists, but is empty, abort 412.
        # movie must have at least one actor
        if len(cast_list) == 0:
            abort(412)
        #
        # ensure all actor ids are valid
        for actor_id in cast_list:
            check_id = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if not check_id:
                abort(412)
        #
        # instantiate new Movie
        new_movie = Movie(title=title, release_date=release_date)
        #
        # attempt to add movie and associated N:M relationships with cast
        try:
            new_movie.insert(cast_list)
            return jsonify({
                'success': True,
                'movie_id': new_movie.id
            })
        except Exception:
            print("aborting in main")
            abort(422)

    # add actor route handler
    # if all fields are not presented by json, abort 412
    # otherwise attempt to add new actor to database
    # if not successful, abort 422
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(jwt):
        json_input = request.get_json()
        name = json_input.get('name')
        dob = json_input.get('dob')
        gender = json_input.get('gender')
        #
        # if any fields are blank, abort 412 (even though
        # from end should catch this, I don't want to assume
        # that is the case)
        if (name is None or dob is None or gender is None):
            abort(412)
        #
        # instantiate new Actor
        new_actor = Actor(name=name, dob=dob, gender=gender)
        #
        # attempt to add to database
        try:
            new_actor.insert()
            return jsonify({
                'success': True,
                'actor_id': new_actor.id
            })
        except Exception:
            abort(422)

    # --------------------------------------------------------------------
    # DELETE handlers
    # --------------------------------------------------------------------

    # delete movie route handler
    # N:M records automatically removed by SQLAlchemy ORM
    # based on definitions established in Class/Model definitions
    # if movie_id doesn't exist, abort 412
    @app.route('/movies/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        movie_to_delete = Movie.query.get(movie_id)
        # if movie id is not found, abort 412
        if movie_to_delete is None:
            abort(412)
        # attempt to delete movie
        try:
            movie_to_delete.delete()
            return jsonify({
                'success': True
            })
        except Exception:
            abort(422)

    # delete actor route handler
    # N:M records automatically removed by SQLAlchemy ORM
    # based on definitions established in Class/Model definitions
    # if actor_id doesn't exist, abort 412
    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
        actor_to_delete = Actor.query.get(actor_id)
        # if actor id is not found, abort 412
        if actor_to_delete is None:
            abort(412)
        # attempt to delete actor
        try:
            actor_to_delete.delete()
            return jsonify({
                'success': True
            })
        except Exception:
            abort(422)

    # --------------------------------------------------------------------
    # PATCH handlers
    # --------------------------------------------------------------------

    # update movie route handler
    # user may update title, release date, and/or list of actors
    # if movie id not found, abort 412
    # if json is empty or does not include at least one of these fields
    # abort 412
    @app.route('/movies/<movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, movie_id):
        movie_to_update = Movie.query.get(movie_id)
        # if movie id not found, abort 412
        if movie_to_update is None:
            abort(412)
        #
        # retrieve json body
        json_input = request.get_json()
        title = json_input.get('title')
        release_date = json_input.get('release_date')
        cast_list = json_input.get('cast')
        #
        # if no fields are present, then abort 412. nothing to update
        if (title is None and release_date is None and cast_list is None):
            abort(412)
        #
        # update fields that have json entries
        if title is not None:
            movie_to_update.title = title

        if release_date is not None:
            movie_to_udpate.release_date = release_date

        if cast_list is not None:
            # ensure cast_list is not empty
            if len(cast_list) == 0:
                abort(412)
            # ensure all new actor ids are valid
            for actor_id in cast_list:
                check_id = (Actor.query.filter(Actor.id == actor_id).
                            one_or_none())
                if not check_id:
                    abort(412)
        #
        # attempt to update movie and associated N:M relationships with cast
        try:
            movie_to_update.update(cast_list)
            return jsonify({
                'success': True,
            })
        except Exception:
            abort(422)

    # update actor route handler
    # user may update name, date of birth, and/or gender
    # if actor id not found, abort 412
    # if json is empty or does not include at least one of these fields
    # abort 412
    @app.route('/actors/<actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, actor_id):
        actor_to_update = Actor.query.get(actor_id)
        # if actor id not found, abort 412
        if actor_to_update is None:
            abort(412)
        #
        # retrieve json body
        json_input = request.get_json()
        name = json_input.get('name')
        dob = json_input.get('dob')
        gender = json_input.get('gender')
        #
        # if no fields are present, then abort 412. nothing to update
        if (name is None and dob is None and gender is None):
            abort(412)
        #
        # update fields that have json entries
        if name is not None:
            actor_to_update.name = name

        if dob is not None:
            actor_to_update.dob = dob

        if gender is not None:
            actor_to_update.gender = gender
        #
        # attempt to update actor record
        try:
            actor_to_update.update()
            return jsonify({
                'success': True,
            })
        except Exception:
            abort(422)

    #####################################################################
    # error handlers
    #####################################################################
    #
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized access"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(412)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 412,
            "message": "precondition failed or request data missing"
        }), 412

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    # authentication error handler
    @app.errorhandler(AuthError)
    def autherror(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code
    #
    # return the app
    return app


#
# instantiate flask app
app = create_app()
#
# run main app
if __name__ == '__main__':
    app.run()
