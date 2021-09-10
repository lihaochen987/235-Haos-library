from library.adapters.repository import AbstractRepository
from library.adapters.jsondatareader import BooksJSONReader
from typing import List
from library.domain.model import Book, BooksInventory, Author
from pathlib import Path


class MemoryRepository(AbstractRepository):
    def __init__(self, *args):
        self._books: List[Book] = list()

        for book in args:
            self._books.append(book)

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self):
        if self._current >= len(self._books):
            raise StopIteration
        else:
            self._current += 1
            return self._books[self._current - 1]
