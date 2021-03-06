from sqlalchemy import (
    Table, MetaData, Column, Integer, String, DateTime, Boolean,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import mapper, relationship, synonym

from library.domain import model

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

publishers_table = Table(
    'publishers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(1024), nullable=True)
)

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
)

books_table = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(1024), nullable=False),
    Column('description', String(1024), nullable=True),
    Column('image_url', String(1024), nullable=False),
    Column('publisher_id', ForeignKey('publishers.id')),
    Column('release_year', Integer, nullable=True),
    Column('ebook', Boolean, nullable=False),
    Column('num_pages', Integer, nullable=True),
    Column('similar_books', ForeignKey('books.id'))
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('book_id', ForeignKey('books.id')),
    Column('review_text', String(1024), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

authors_table = Table(
    'authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(1024), nullable=False),
)

# Relational mappers for many to many relationships

books_authors_table = Table(
    'books_authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', ForeignKey('books.id')),
    Column('author_id', ForeignKey('authors.id'))
)

similar_books_table = Table(
    'similar_books', metadata,
    Column('id', Integer, primary_key=True, autoincrement = True),
    Column('book_id', ForeignKey('books.id')),
    Column('similar_book_id', ForeignKey('books.id')),
    UniqueConstraint('book_id', 'similar_book_id', name = 'similar_books')
)

def map_model_to_tables():
    mapper(model.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(model.Review, back_populates='_Review__user')
    })
    mapper(model.Review, reviews_table, properties={
        '_Review__user': relationship(model.User, back_populates='_User__reviews'),
        '_Review__book': relationship(model.Book, back_populates='_Book__reviews'),
        '_Review__review_text': reviews_table.c.review_text,
        '_Review__rating': reviews_table.c.rating,
        '_Review__timestamp': reviews_table.c.timestamp
    })
    mapper(model.Author, authors_table, properties={
        '_Author__unique_id': authors_table.c.id,
        '_Author__full_name': authors_table.c.full_name,
        '_Author__books': relationship(model.Book, secondary=books_authors_table, back_populates='_Book__authors')
    })
    mapper(model.Publisher, publishers_table, properties = {
        '_Publisher__books': relationship(model.Book, back_populates = '_Book__publisher'),
        '_Publisher__name': publishers_table.c.name
    })
    mapper(model.Book, books_table, properties={
        '_Book__book_id': books_table.c.id,
        '_Book__title': books_table.c.title,
        '_Book__image_url': books_table.c.image_url,
        '_Book__description': books_table.c.description,
        '_Book__authors': relationship(model.Author, secondary=books_authors_table, back_populates='_Author__books'),
        '_Book__publisher':relationship(model.Publisher, back_populates='_Publisher__books'),
        '_Book__release_year': books_table.c.release_year,
        '_Book__ebook': books_table.c.ebook,
        '_Book__num_pages': books_table.c.num_pages,
        '_Book__reviews': relationship(model.Review, back_populates='_Review__book'),
        '_Book__similar_books': relationship(model.Book, secondary = similar_books_table, primaryjoin=books_table.c.id == similar_books_table.c.book_id, secondaryjoin = books_table.c.id == similar_books_table.c.similar_book_id)
    })
