# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, request, url_for, g
from app import app, models
from forms import LoginForm
from flask_login import login_user, logout_user, current_user, login_required
from hashlib import md5


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
def index():
    books = models.Book.query.all()
    return render_template("index.html",
                           title='Home',
                           books=books)


@app.route('/book/<id>')
def book(id):
    book = models.Book.query.get(int(id))
    if book is None:
        flash('Book not found')
        return redirect(url_for('index'))
    return render_template('book.html', book=book)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        login = request.form['login']
        password = request.form['password']
        m = md5()
        m.update(password)
        registered_user = models.User.query.filter_by(login=login, password=m.hexdigest()).first()

        if registered_user is None:
            flash('Username or Password is invalid', 'error')
            return redirect(url_for('login'))

        login_user(registered_user)
        flash('Logged in successfully')

        return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# @app.route('/register' , methods=['GET','POST'])
# def register():
#     if request.method == 'GET':
#         return render_template('register.html')
#     user = models.User(request.form['username'] , request.form['password'],request.form['email'])
#     db.session.add(user)
#     db.session.commit()
#     flash('User successfully registered')
#     return redirect(url_for('login'))


@app.route("/all-links")
def all_links():
    import urllib
    links = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = [urllib.unquote(url), rule.endpoint, methods]
        links.append(line)

    return render_template("all_links.html", links=links)