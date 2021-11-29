from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


# DB_PATH = "postgresql://gfcflfufocxlyz:6f25ba25448586e64005868c0e09bc06e5c21d6b141d774e7c9b4db9f85f13db@ec2-18-210" \
#           "-159-154.compute-1.amazonaws.com:5432/df9ngni1g2mbok"
DB_PATH = "postgresql://postgres:1@localhost:5432/theater"
db = SQLAlchemy()


def db_setup(app, database_path=DB_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # add one demo row which is helping in POSTMAN test
    theater_1 = Theater(name='a', city='a', state='a', address='a', phone='a', website='a')
    theater_2 = Theater(name='b', city='b', state='b', address='b', phone='b', website='b')
    movie_1 = Movie(title='a', image_link='a', trailer='a', review='a', description='a')
    movie_2 = Movie(title='b', image_link='b', trailer='b', review='b', description='b')
    show_1 = Showtime(
        theater_id=1,
        movie_id=1,
        start_time=['12:00', '14:30']
    )
    show_2 = Showtime(
        theater_id=2,
        movie_id=2,
        start_time=['13:00', '15:30']
    )
    theater_1.insert()
    theater_2.insert()
    movie_1.insert()
    movie_2.insert()
    show_1.insert()
    show_2.insert()


class Theater(db.Model):
    __tablename__ = 'theaters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    showtimes = db.relationship(
        'Showtime',
        backref=db.backref('theater', lazy=True),
        cascade="all, delete"
    )

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    image_link = db.Column(db.String(120))
    trailer = db.Column(db.String(500))
    review = db.Column(db.String(120))
    description = db.Column(db.String(500))
    showtimes = db.relationship(
        'Showtime',
        backref=db.backref('movie', lazy=True),
        cascade="all, delete"
    )

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Showtime(db.Model):
    __tablename__ = 'showtimes'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.ARRAY(db.String), nullable=False)
    theater_id = db.Column(
        db.Integer,
        db.ForeignKey('theaters.id'),
        nullable=False,
    )
    movie_id = db.Column(
        db.Integer,
        db.ForeignKey('movies.id'),
        nullable=False,
    )

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
