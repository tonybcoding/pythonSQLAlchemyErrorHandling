#########################################################################
#
# @file name: models.py
# @purpose: establish SQLAlchemy ORM session, define all classes and
#  associated properties/methods
# @author: Tony Burge
# @date: 2020-09-08
# @credits: SQLAlchemy setup_db taken directly from Udacity FSND
#  coursework
#
#########################################################################
#
# global imports
import os
from sqlalchemy import Column, String, Integer, Date
from flask_sqlalchemy import SQLAlchemy
import json
#
# if os variable not set, use local instance
database_path = os.environ.get('DATABASE_URL')
if not database_path:
    database_name = "casting"
    database_path = "postgres://{}/{}".format('localhost:5432', database_name)
#
# instantiate SQLAlchemy
db = SQLAlchemy()
#
# function to bind flask app with SQLAlchemy session
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

#
#########################################################################
# Model and Class definitions
#########################################################################
#
# implementing many-to-many (or N:M) relationships between movies and actors
# as one movie contains one or more actors, and each actor can be part of
# 0, 1, or many movies
#
# movie.id and actor.id are lower case since they refer to the table names
# movie and actor and not the class names Movie/Actor
moviecast = db.Table('moviecast',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'))
)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.Date)
    # add connection to N:M table with an attribute castmembers
    # and a "virtual" propert in Actor called "movies", so we can access with
    # actor.movies
    castmembers = db.relationship('Actor', secondary=moviecast,
        cascade = "all,delete",
        backref=db.backref('movies', lazy='dynamic')
    )

    # methods to insert, delete, and update Movie objects
    def insert(self, cast_list):
        try:
            db.session.add(self)
            # add N:M relationships
            for actor_id in cast_list:
                this_actor = Actor.query.filter(Actor.id == actor_id).one()
                this_actor.movies.append(self)
            db.session.commit()
        except:
            db.session.rollback()
            print("aborting in models")
            abort(422)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            abort(422)

    def update(self, cast_list):
        try:
            # if cast_list is populated, remove previous actors and
            # add new ones (cast_list is passed as long as at least
            # one of the fields in update_movie is included)
            if cast_list is not None:
                self.castmembers = []
                for actor_id in cast_list:
                    this_actor = Actor.query.filter(Actor.id == actor_id).one()
                    print("adding", this_actor.name)
                    this_actor.movies.append(self)
            # commit changes            
            db.session.commit()
        except:
            db.session.rollback()
            abort(422)


# please note, I implemented date of birth instead of age
# as dob can be used to dynamically calculate age
class Actor(db.Model):
    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    dob = db.Column(db.Date)
    gender = db.Column(db.String)

    # methods to insert, delete, and update Movie objects
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            abort(422)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            abort(422)

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            abort(422)

    # returns a formatted dictionary entry of the actor object
    def create_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "dob": self.dob,
            "gender": self.gender            
        }
