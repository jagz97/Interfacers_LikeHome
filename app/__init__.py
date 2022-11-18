
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_msearch import Search
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='you-will-never-know',
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'test.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# Flask-Uploads configuration provided on Documentation Page
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(basedir, 'static/img')

# Photo Upload Setup Sourced from FLASK_UPLOADS Documentation page https://pythonhosted.org/Flask-Uploads/
photos = UploadSet('photos', IMAGES)  # Flask-Uploads Upload Sets
configure_uploads(app, photos)

db = SQLAlchemy(app)
search = Search()
search.init_app(app)  # initialize search

login = LoginManager(app)
login.login_view = 'login'

# adds admin functionality and page to flask app
def add_admin(app):
    from .AdminView import AdminView
    from .AdminTabView import AdminTabView
    from flask_admin import Admin
    from .models import Reservations, User

    # https://ckraczkowsky.medium.com/building-a-secure-admin-interface-with-flask-admin-and-flask-security-13ae81faa05
    admin = Admin(app, index_view=AdminTabView())
    admin.add_view(AdminView(Reservations, db.session))
    admin.add_view(AdminView(User, db.session))

add_admin(app)

from app import routes