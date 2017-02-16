from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired


class AddBookForm(FlaskForm):
    isbn = StringField('isbn', validators=[DataRequired()])
