CSRF_ENABLED = True
SECRET_KEY = ''

import os
_basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = ''
SQLALCHEMY_MIGRATE_REPO = os.path.join(_basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

try:
    from private import *
except Exception:
    pass

print SECRET_KEY