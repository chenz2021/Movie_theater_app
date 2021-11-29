import os
from flask import Flask, request, jsonify, abort
# from flask import render_template, session, url_for, redirect
from sqlalchemy import exc
import json
from flask_cors import CORS
from models import db_setup, Theater, Movie, Showtime
from auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    db = db_setup(app)
    CORS(app)

    # db_drop_and_create_all()
    @app.after_request
    def after_request(response):

        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')

        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': 'Welcome to the movie theater!'})

    @app.route('/movies', methods=['GET'])
    def get_movies():
        movies = Movie.query.order_by(Movie.id).all()
        data = []
        for movie in movies:
            temp_data = {
                'movie_id': movie.id,
                'movie_image': movie.image_link,
                'movie_trailer': movie.trailer,
                'movie_review': movie.review,
                'movie_description': movie.description
            }
            data.append(temp_data)
        return jsonify({
            'success': True,
            'movie_info': data
        })

    @app.route('/movies/<movie_id>', methods=['GET'])
    def get_movies_by_id(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        data = []
        shows = Showtime.query.join(Movie, Movie.id == Showtime.movie_id). \
            filter(Movie.id == movie_id).all()
        for show in shows:
            temp_show = {
                'theater_id': show.theater_id,
                'theater_name': show.theater.name,
                'address': show.theater.address,
                'website': show.theater.website,
                'showtime': show.start_time
            }
            data.append(temp_show)
        return jsonify({
            'success': True,
            'showtime_info': data
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movie(jwt):
        body = request.get_json()
        title = body.get('title', None)
        image_link = body.get('image_link', None)
        trailer = body.get('trailer', None)
        review = body.get('review', None)
        description = body.get('description', None)
        try:
            movie = Movie(
                title=title,
                image_link=image_link,
                trailer=trailer,
                review=review,
                description=description
            )
            movie.insert()
            return jsonify({
                'success': True,
                'added': movie.id
            })
        except Exception:
            abort(400)

    @app.route('/movies/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(jwt, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        try:
            movie.delete()
            return jsonify({
                'success': True,
                'delete': movie_id
            }, 200)
        except:
            abort(422)

    @app.route('/movies/search', methods=['POST'])
    def search_movies():
        body = request.get_json()
        search_term = body.get('search_term', '')
        movies = Movie.query.filter(Movie.title.ilike('%' + search_term + '%')).all()
        response = {
            'count': len(movies),
            'data': []
        }
        for movie in movies:
            response['data'].append({
                'id': movie.id,
                'title': movie.title
            })
        return jsonify({
            'success': True,
            'response': response
        })

    @app.route('/theaters', methods=['GET'])
    def get_theaters():
        theaters = Theater.query.order_by(Theater.id).all()
        data = []
        for theater in theaters:
            temp_data = {
                'theater_id': theater.id,
                'theater_name': theater.name,
                'theater_address': theater.address,
                'theater_phone': theater.phone,
                'theater_website': theater.website
            }
            data.append(temp_data)
        return jsonify({
            'success': True,
            'movie_info': data
        })

    @app.route('/theaters/<theater_id>', methods=['GET'])
    def get_theaters_by_id(theater_id):
        theater = Theater.query.filter(Theater.id == theater_id).one_or_none()
        if theater is None:
            abort(404)
        data = []
        shows = Showtime.query.join(Theater, theater.id == Showtime.theater_id). \
            filter(Theater.id == theater_id).all()
        for show in shows:
            temp_show = {
                'movie_id': show.movie_id,
                'movie_title': show.movie.title,
                'movie_image': show.movie.image_link,
                'trailer': show.movie.trailer,
                'review': show.movie.review,
                'showtime': show.start_time
            }
            data.append(temp_show)
        return jsonify({
            'success': True,
            'showtime_info': data
        })

    @app.route('/theaters/<theater_id>', methods=['PATCH'])
    @requires_auth('patch:theaters')
    def update_theaters_by_id(jwt, theater_id):
        theater = Theater.query.filter(Theater.id == theater_id).one_or_none()
        if theater is None:
            abort(404)
        body = request.get_json()

        theater.name = body.get('name', None)
        theater.city = body.get('city', None)
        theater.state = body.get('state', None)
        theater.address = body.get('address', None)
        theater.phone = body.get('phone', None)
        theater.website = body.get('website', None)
        try:
            theater.update()
            return jsonify({
                'success': True,
                'updated': theater.id
            }, 200)
        except:
            abort(422)

    @app.route('/theaters', methods=['POST'])
    @requires_auth('post:theaters')
    def post_theater(jwt):
        body = request.get_json()
        name = body.get('name', None)
        city = body.get('city', None)
        state = body.get('state', None)
        address = body.get('address', None)
        phone = body.get('phone', None)
        website = body.get('website', None)
        try:
            theater = Theater(
                name=name,
                city=city,
                state=state,
                address=address,
                phone=phone,
                website=website
            )
            theater.insert()
            return jsonify({
                'success': True,
                'added': theater.id
            })
        except Exception:
            abort(400)

    @app.route('/theaters/<theater_id>', methods=['DELETE'])
    @requires_auth('delete:theaters')
    def delete_theaters(jwt, theater_id):
        theater = Theater.query.filter(Theater.id == theater_id).one_or_none()
        if theater is None:
            abort(404)
        try:
            theater.delete()
            return jsonify({
                'success': True,
                'delete': theater_id
            }, 200)
        except:
            abort(422)

    @app.route('/showtimes/create', methods=['POST'])
    @requires_auth('post:showtimes')
    def create_showtime(jwt):
        error = False
        body = request.get_json()
        movie_id = body.get('movie_id', None)
        theater_id = body.get('theater_id', None)
        start_time = body.get('start_time', None)
        try:
            show = Showtime(
                theater_id=theater_id,
                movie_id=movie_id,
                start_time=start_time,
            )
            show.insert()
            return jsonify({
                'success': True
            })
        except Exception:
            abort(400)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "forbidden"
        }), 403

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(AuthError)
    def process_AuthError(error):
        response = jsonify(error.error)
        response.status_code = error.status_code

        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
