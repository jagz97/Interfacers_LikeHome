from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, false
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
import json
from flask_login import UserMixin
from sqlalchemy import create_engine
import csv
import pandas
from datetime import datetime








engine = create_engine('sqlite:///hotels.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.



class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class Reservations(db.Model):
    __searchable__ = ['username']
    id = db.Column(db.Integer, primary_key=True)
    hotelName = db.Column(db.String(80), nullable=False)
    hotelId = db.Column(db.String(1000), nullable=False)
    # Integer with 2 decimal places
    price = db.Column(db.Numeric(10, 2), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    username = db.Column(db.String(32), nullable=False)
 
    def __repr__(self):
        return '<Reservations {}>'.format(self.username)


class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.name)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))
# Create tables.

Base.metadata.create_all(bind=engine)
db.create_all()

file_name = "app/data1.csv"

df = pandas.read_csv(file_name)


