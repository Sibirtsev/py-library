from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from jinja2 import TemplateNotFound
from flask_login import login_required
from flask_navigation import Navigation
from forms import AddBookForm
from app import models
import isbnlib

admin_page = Blueprint('admin_page', __name__, template_folder='templates/admin')

admin_nav = Navigation()
admin_nav.Bar('top', [
    admin_nav.Item('Dashboard', 'admin_page.index'),
    admin_nav.Item('Public', 'index'),
    admin_nav.Item('Logout', 'logout')
])

admin_nav.Bar('left', [
    admin_nav.Item('Overview', 'admin_page.index'),
    admin_nav.Item('Books', 'admin_page.books'),
    admin_nav.Item('Authors', 'admin_page.index'),
    admin_nav.Item('Users', 'admin_page.index'),
])


@admin_page.route('/')
@admin_page.route('/index')
@login_required
def index():
    try:
        return render_template('admin/base.html')
    except TemplateNotFound:
        abort(404)


@admin_page.route('/books')
@login_required
def books():
    books_list = models.Book.query.all()
    return render_template('admin/books.html', books=books_list)


@admin_page.route('/books/add', methods=['GET', 'POST'])
@login_required
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        isbn = request.form['isbn']
        if isbnlib.is_isbn13(isbn):
            isbn = isbnlib.to_isbn10(isbn)
        if not isbnlib.is_isbn10(isbn):
            flash('Enter valid ISBN', 'error')
            return redirect(url_for('admin_page.add_book'))

        book_data = isbnlib.meta(isbn)
        book_cover = isbnlib.cover(isbn)
