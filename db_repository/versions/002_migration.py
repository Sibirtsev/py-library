from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
author = Table('author', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name_en', String(length=120)),
    Column('name_ru', String(length=120)),
    Column('bio', Text),
)

book = Table('book', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('isbn', String(length=13)),
    Column('title', String(length=255)),
)

book_by_author = Table('book_by_author', post_meta,
    Column('book_id', Integer),
    Column('author_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['author'].create()
    post_meta.tables['book'].create()
    post_meta.tables['book_by_author'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['author'].drop()
    post_meta.tables['book'].drop()
    post_meta.tables['book_by_author'].drop()
