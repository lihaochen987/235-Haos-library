from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy import update
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from library.adapters.repository import AbstractRepository
from library.domain.model import User, Book, Review, Author, Publisher

from flask import _app_ctx_stack


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def __len__(self):
        number_of_books = self._session_cm.session.query(Book).count()
        return number_of_books

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self):
        if self._current >= self._session_cm.session.query(Book).count():
            raise StopIteration
        else:
            self._current += 1
            return self._session_cm.session.query(Book).slice(0, self._current - 1)

    def offset(self, offset, per_page):
        return self._session_cm.session.query(Book).slice(offset, offset + per_page)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    # Testing purposes
    def get_books(self):
        return self._session_cm.session.query(Book).all()

    def get_number_of_books(self):
        number_of_books = self._session_cm.session.query(Book).count()
        return number_of_books

    def add_author(self, author:Author):
        with self._session_cm as scm:
            scm.session.add(author)
            scm.commit()

    def add_publisher(self, publisher:Publisher):
        with self._session_cm as scm:
            scm.session.add(publisher)
            scm.commit()

    def add_similar_book(self, book_one:Book, book_two:Book):
        similar_book_one = self._session_cm.session.query(Book).filter(Book._Book__book_id == book_one.book_id).all()
        similar_book_two = self._session_cm.session.query(Book).filter(Book._Book__book_id == book_two.book_id).all()

        similar_book_one[0].similar_books = similar_book_two[0]
        similar_book_two[0].similar_books = similar_book_one[0]

        self._session_cm.commit()

    # Book functions
    def add_book(self, book: Book):
        with self._session_cm as scm:
            scm.session.add(book)
            scm.commit()

    def get_book_by_id(self, book_id: int):
        books_list = []
        try:
            books_list = self._session_cm.session.query(Book).filter(Book._Book__book_id == book_id).all()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return books_list

    def get_book_by_title(self, title: str):
        books_list = []
        try:
            books_list = self._session_cm.session.query(Book).filter(Book._Book__title == title).all()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return books_list

    def get_book_by_author(self, author_name: str):
        books_list = []
        try:
            books_list = self._session_cm.session.query(Book).join(Author, Book._Book__authors.any(Author._Author__full_name == author_name)).all()

        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return books_list

    def get_book_by_publisher(self, publisher_name: str):
        books_list = []
        try:
            books_list = self._session_cm.session.query(Book).join(Publisher, Book._Book__publisher.has(Publisher._Publisher__name == publisher_name)).all()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return books_list

    def get_book_by_release_year(self, year: int):
        books_list = []
        try:
            books_list = self._session_cm.session.query(Book).filter(Book._Book__release_year == year).all()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return books_list


    def get_reviews(self):
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()
