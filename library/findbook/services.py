from typing import List, Iterable

from library.adapters.repository import AbstractRepository
from library.domain.model import leave_review, Review, Book


class NonExistentBookException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_book_by_id(book_id: int, repo: AbstractRepository):
    books = repo.get_book_by_id(book_id)
    if books == None:
        return None
    return books[0]


def get_book_by_title(book_title: str, repo: AbstractRepository):
    books = repo.get_book_by_title(book_title)
    return books


def get_book_by_author(author_name: str, repo: AbstractRepository):
    books = repo.get_book_by_author(author_name)
    return books


def get_book_by_publisher(publisher_name: str, repo: AbstractRepository):
    books = repo.get_book_by_publisher(publisher_name)
    return books


def get_book_by_release_year(year: int, repo: AbstractRepository):
    books = repo.get_book_by_release_year(year)
    return books


def get_book_by_ebook_status(e_book_status: bool, repo: AbstractRepository):
    books = repo.get_book_by_ebook_status(e_book_status)
    return books


def get_book_by_number_of_pages(pages: int, repo: AbstractRepository):
    books = repo.get_book_by_number_of_pages(pages)
    return books