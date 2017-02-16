from app import db

ROLE_READER = 0
ROLE_LIBRARIAN = 1
ROLE_ADMIN = 2


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(32), index=True, unique=False)
    role = db.Column(db.SmallInteger, default=ROLE_READER)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User login={}, role={}>'.format(self.login, self.role)


books_by_author = db.Table('book_by_author',
                           db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
                           db.Column('author_id', db.Integer, db.ForeignKey('author.id')))

books_by_tag = db.Table('book_by_tag',
                        db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
                        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), index=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text())
    publisher = db.relationship('Publisher', backref=db.backref('books', lazy='dynamic'))
    authors = db.relationship("Author", secondary=books_by_author,
                              backref=db.backref('books', lazy='dynamic'))
    tags = db.relationship("Tag", secondary=books_by_tag,
                           backref=db.backref('books', lazy='dynamic'))

    def __repr__(self):
        return '<Book isbn={}, title={}>'.format(self.isbn.encode('utf8'), self.title.encode('utf8'))


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(120))
    name_ru = db.Column(db.String(120))
    bio = db.Column(db.Text())

    def __repr__(self):
        return '<Author name_en={}, name_ry={}>'.format(self.name_en.encode('utf8'), self.name_ru.encode('utf8'))


class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100))

    def __repr__(self):
        return '<Tag {}>'.format(self.tag.encode('utf8'))
