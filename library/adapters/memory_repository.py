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

    def add_book(self, book: Book):
        self._books.append(book)

    def get_book_by_id(self, id: int):
        for book in self._books:
            if book.book_id == id:
                return book

    def get_book_by_title(self, title:str):
        books_list = []
        for book in self._books:
            if book.title == title:
                books_list.append(book)
        return books_list

    def get_book_by_author(self, author_name:str):
        books_list = []
        for book in self._books:
            for author in book.authors:
                if author.full_name == author_name:
                    books_list.append(book)
        return books_list