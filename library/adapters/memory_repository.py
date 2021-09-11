from library.adapters.repository import AbstractRepository
from library.adapters.jsondatareader import BooksJSONReader
from typing import List
from library.domain.model import Book, BooksInventory, Author, User
from pathlib import Path


class MemoryRepository(AbstractRepository):
    def __init__(self, *args):
        self._books: List[Book] = list()

        for book in args:
            self._books.append(book)

        self.__users = list()

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self):
        if self._current >= len(self._books):
            raise StopIteration
        else:
            self._current += 1
            return self._books[self._current - 1]

    # Book functions
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

    def get_book_by_publisher(self, publisher_name:str):
        books_list = []
        for book in self._books:
                if book.publisher.name == publisher_name:
                    books_list.append(book)
        return books_list

    def get_book_by_release_year(self, year:int):
        books_list = []
        for book in self._books:
            if book.release_year == year:
                books_list.append(book)
        return books_list

    def get_book_by_ebook_status(self, e_book_status:bool):
        books_list = []
        for book in self._books:
            if book.ebook == e_book_status:
                books_list.append(book)
        return books_list

    def get_book_by_number_of_pages(self, pages:int):
        books_list = []
        for book in self._books:
            if book.num_pages == pages:
                books_list.append(book)
        return books_list

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)