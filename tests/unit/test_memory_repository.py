from datetime import date, datetime
from typing import List

import pytest

from library.domain.model import Book
from library.adapters.repository import RepositoryException

# some_book = Book(1, "Harry Potter and the Chamber of Secrets")
# some_book.description = "Ever since Harry Potter had come home for the summer, the Dursleys had been so mean \
#                          and hideous that all Harry wanted was to get back to the Hogwarts School for \
#                          Witchcraft and Wizardry. But just as he’s packing his bags, Harry receives a \
#                          warning from a strange impish creature who says that if Harry returns to Hogwarts, \
#                          disaster will strike."
# some_book.release_year = 1999

def test_repository_can_get_book_by_id(in_memory_repo):
    some_book = Book(1, "Harry Potter and the Chamber of Secrets")
    in_memory_repo.add_book(some_book)
    assert in_memory_repo.get_book_by_id(1) is some_book