# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")



class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


"""Схемы для сериализации модели"""
class MovieSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    description = fields.String()
    trailer = fields.String()
    year = fields.Integer()
    rating = fields.Float()
    genre = fields.String()
    genre_id = fields.Integer()
    director = fields.String()
    director_id = fields.Integer()


class DirectorSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class GenreSchema(Schema):
    id = fields.Integer()
    name = fields.String()


"""Создание объектов"""
movie_schema = MovieSchema()
director_schema = DirectorSchema()
genre_schema = GenreSchema()


""""""
api = Api(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


"""Movies"""
@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        i = Movie.query
        if director_id is not None:
            i = i.filter(Movie.director_id == director_id)
        if genre_id is not None:
            i = i.filter(Movie.genre_id == genre_id)
        if director_id is not None and genre_id is not None:
            i = i.filter(Movie.director_id == director_id and Movie.genre_id == genre_id)
        result = i.all()

        return movie_schema.dump(result, many=True)

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


@movie_ns.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid: int):
        try:
            movie = Movie.query.get(uid)
            return movie_schema.dump(movie)
        except Exception as e:
            return "", 404

    def delete(self, uid: int):
        movie = Movie.query.get(uid)
        db.session.delete(movie)
        db.session.commit()
        return "", 204

    def put(self, uid):
        movie = Movie.query.get(uid)
        if not movie:
            return "", 404
        req_json = request.json
        movie.id = req_json.get("id")
        movie.title = req_json.get("GOVNO")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre = req_json.get("genre")
        movie.genre_id = req_json.get("genre_id")
        movie.director = req_json.get("director")
        movie.director_id = req_json.get("director_id")
        db.session.add(movie)
        db.session.commit()
        return "", 204


"""Directors"""
@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = Director.query.all()
        return director_schema.dump(directors, many=True)

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return "", 201

@director_ns.route('/<int:uid>')
class DirectorView(Resource):
    def get(self, uid: int):
        try:
            director = Director.query.get(uid)
            return director_schema.dump(director)
        except Exception as e:
            return "", 404

    def delete(self, uid: int):
        director = Director.query.get(uid)
        db.session.delete(director)
        db.session.commit()
        return "", 204

    def put(self, uid):
        director = Director.query.get(uid)
        if not director:
            return "", 404
        req_json = request.json
        director.id = req_json.get("id")
        director.name = req_json.get("name")
        db.session.add(director)
        db.session.commit()
        return "", 204


"""Genres"""
@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = Genre.query.all()
        return genre_schema.dump(genres, many=True)

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return "", 201

@genre_ns.route('/<int:uid>')
class GenreView(Resource):
    def get(self, uid: int):
        try:
            genre = Genre.query.get(uid)
            return genre_schema.dump(genre)
        except Exception as e:
            return "", 404

    def delete(self, uid: int):
        genre = Genre.query.get(uid)
        db.session.delete(genre)
        db.session.commit()
        return "", 204

    def put(self, uid):
        genre = Genre.query.get(uid)
        if not genre:
            return "", 404
        req_json = request.json
        genre.id = req_json.get("id")
        genre.name = req_json.get("name")
        db.session.add(genre)
        db.session.commit()
        return "", 204

if __name__ == '__main__':
    app.run(debug=True)
