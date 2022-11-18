from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from sqlalchemy import event
from werkzeug.security import generate_password_hash



class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('/login'))
