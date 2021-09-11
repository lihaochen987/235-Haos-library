import abc
from typing import List
from datetime import date

from library.domain.model import Book, Author


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def __iter__(selfs):
        """ Loops through the abstract repository """
        raise NotImplementedError

    @abc.abstractmethod
    def __next__(self) -> Book:
        """ Gets next book object from repository """
        raise NotImplementedError

    # Book functions
    @abc.abstractmethod
    def add_book(self, book: Book):
        """ Adds a book object to our library """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_by_id(self, id: int):
        """" Gets a book by specified id (UNIQUE) """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_by_title(self, title:str):
        """ Gets book/s by specified title (NOT UNIQUE) """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_by_author(self, author_name:str):
        """ Gets book/s by specified author (NOT UNIQUE) """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_by_publisher(self, publisher_name:str):
        """ Gets book/s by specified author (NOT UNIQUE) """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_by_release_year(self, year:int):
        """ Gets book/s by specified release year (NOT UNIQUE) """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_by_ebook_status(self, e_book_status:bool):
        """ Gets book/s by specified e_book status (NOT UNIQUE) """
        raise NotImplementedError



