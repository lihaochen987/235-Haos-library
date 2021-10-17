import abc
from typing import List
from datetime import date

from library.domain.model import Book, User, Review, Author, Publisher

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    # @abc.abstractmethod
    # def __iter__(selfs):
    #     """
    #     Loops through the abstract repository
    #      """
    #     raise NotImplementedError
    #
    # @abc.abstractmethod
    # def __next__(self) -> Book:
    #     """
    #     Gets next book object from repository
    #     """
    #     raise NotImplementedError

    # Methods for testing purposes
    @abc.abstractmethod
    def get_books(self):
        """
        Gets all books from the repository
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_books(self) -> int:
        """
        Gets number of books in the repository
        """
        raise NotImplementedError

    # Book methods
    @abc.abstractmethod
    def add_book(self, book: Book):
        """
        Adds a book object to our library
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_by_id(self, id: int):
        """"
        Gets a book by specified id (UNIQUE)
        If there is no Book with the given book_id, this method returns None.
         """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_by_title(self, title: str):
        """
        Gets book/s by specified title (NOT UNIQUE)
        If there is no Book with the given title, this method returns None.
         """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_by_author(self, author_name: str):
        """
        Gets book/s by specified author (NOT UNIQUE)
        If there is no Book with the given author, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_by_publisher(self, publisher_name: str):
        """
        Gets book/s by specified author (NOT UNIQUE)
        If there is no Book with the given publisher, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_by_release_year(self, year: int):
        """
        Gets book/s by specified release year (NOT UNIQUE)
        If there is no Book with the given release year, this method returns None.
        """
        raise NotImplementedError

    # User methods
    @abc.abstractmethod
    def add_user(self, user: User):
        """
        Adds a User to the repository
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """
        Returns the User named user_name from the repository.
        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    # Review methods

    @abc.abstractmethod
    def get_reviews(self):
        """
        Returns all reviews stored in the repository
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review:Review):
        """
        Adds a review to a book
        User must be logged in to leave a review
        User must leave a rating of between 1 to 5, the comment is optional
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review.book is None or review not in review.book.reviews:
            raise RepositoryException('Review not correctly attached to a Book')

    @abc.abstractmethod
    def add_author(self, author:Author):
        """
        Adds an author to the repository
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_publisher(self, publisher:Publisher):
        """
        Adds a publisher to the repository
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_similar_book(self, book_one:Book, book_two:Book):
        """
        Adds a similar book to an existing book
        """
        raise NotImplementedError