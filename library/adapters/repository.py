import abc
from typing import List
from datetime import date

from library.domain.model import Book, User, Review

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def __iter__(selfs):
        """
        Loops through the abstract repository
         """
        raise NotImplementedError

    @abc.abstractmethod
    def __next__(self) -> Book:
        """
        Gets next book object from repository
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

    @abc.abstractmethod
    def get_book_by_ebook_status(self, e_book_status: bool):
        """
        Gets book/s by specified e_book status (NOT UNIQUE)
        If there is no Book with the given e_book status, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_by_number_of_pages(self, pages: int):
        """
        Gets book/s by specified number of pages (NOT UNIQUE)
        If there is no Book with the given number of pages, this method returns None.
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
    # @abc.abstractmethod
    # def add_review(self, review:Review):
    #     """
    #     Adds a review to a book
    #     User must be logged in to leave a review
    #     User must leave a rating of between 1 to 5, the comment is optional
    #     """
    #     if review.