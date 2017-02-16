# -*- coding: utf-8 -*-
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')

lm = LoginManager()
lm.login_view = 'login'
lm.init_app(app)

db = SQLAlchemy(app)

from app.admin.views import admin_page, admin_nav

app.register_blueprint(admin_page, url_prefix='/admin')
admin_nav.init_app(app)

from app import views, models


@lm.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

