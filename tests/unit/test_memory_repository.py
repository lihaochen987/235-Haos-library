from datetime import date, datetime
from typing import List

import pytest

from library.domain.model import Book, Author
from library.adapters.repository import RepositoryException


@pytest.fixture()
def book():
    some_book = Book(1, "Harry Potter and the Chamber of Secrets")
    some_author = Author(52, "J. K. Rowling")
    some_book.description = "Ever since Harry Potter had come home for the summer, the Dursleys had been so mean \
                         and hideous that all Harry wanted was to get back to the Hogwarts School for \
                         Witchcraft and Wizardry. But just as he’s packing his bags, Harry receives a \
                         warning from a strange impish creature who says that if Harry returns to Hogwarts, \
                         disaster will strike."
    some_book.release_year = 1999
    some_book.add_author(some_author)
    return some_book


def test_repository_can_get_book_by_id(in_memory_repo, book):
    in_memory_repo.add_book(book)

    assert in_memory_repo.get_book_by_id(1) is book


def test_repository_can_get_book_by_title(in_memory_repo, book):
    in_memory_repo.add_book(book)

    assert in_memory_repo.get_book_by_title("Harry Potter and the Chamber of Secrets")[0] is book


def test_repository_can_get_books_with_same_title(in_memory_repo, book):
    in_memory_repo.add_book(book)

    similar_book = Book(512, "Harry Potter and the Chamber of Secrets")
    in_memory_repo.add_book(similar_book)
    assert in_memory_repo.get_book_by_title("Harry Potter and the Chamber of Secrets")[0] is book
    assert in_memory_repo.get_book_by_title("Harry Potter and the Chamber of Secrets")[1] is similar_book


def test_repository_can_get_book_by_author(in_memory_repo, book):
    in_memory_repo.add_book(book)

    assert in_memory_repo.get_book_by_author("J. K. Rowling")[0] is book


def test_repository_can_get_multiple_books_by_same_author(in_memory_repo, book):
    in_memory_repo.add_book(book)

    another_book = Book(32, "Harry Potter and the Philosopher's Stone")
    author = Author(52, "J. K. Rowling")
    another_book.add_author(author)
    in_memory_repo.add_book(another_book)

    assert in_memory_repo.get_book_by_author("J. K. Rowling")[0] is book
    assert in_memory_repo.get_book_by_author("J. K. Rowling")[1] is another_book
    assert len(in_memory_repo.get_book_by_author("J. K. Rowling")) == 2
