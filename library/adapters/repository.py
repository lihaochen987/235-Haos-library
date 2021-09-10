import abc
from typing import List
from datetime import date

from library.domain.model import Book


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

    @abc.abstractmethod
    def add_book(self, book: Book):
        """ Adds a book object to our library """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_by_id(self, id: int):
        """" Gets a book by specified id """
        raise NotImplementedError






