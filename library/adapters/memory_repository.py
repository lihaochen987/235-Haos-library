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

    def get_book_by_id(self, id: int):
        for book in self._books:
            if book.book_id == id:
                return book

    def add_book(self, book: Book):
        self._books.append(book)