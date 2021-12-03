from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from create_data import *
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


api = Api(app)
movies_ns = api.namespace('movies')


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        return movies_schema.dump(Movie.query.all()), 200


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid: int):
        movie = Movie.query.get(mid)
        if not movie:
            movies_ns.abort(404)
        return movie_schema.dump(movie), 200


@movies_ns.route('/')
class MoviesByDirView(Resource):
    def get(self):
        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")
        if director_id is not None:
            movie = Movie.query.filter(Movie.director_id == director_id)
        if genre_id is not None:
            movie = Movie.query.filter(Movie.genre_id == genre_id)
        movies = movie.all()
        return movies_schema.dump(movies), 200



if __name__ == '__main__':
    app.run(debug=True)
