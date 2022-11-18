from flask import redirect, url_for
from flask_admin import AdminIndexView
from flask_login import current_user


class AdminTabView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
