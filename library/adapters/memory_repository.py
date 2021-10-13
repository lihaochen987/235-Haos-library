from typing import List

from library.adapters.repository import AbstractRepository
from library.domain.model import Book, User, Review, Author


class MemoryRepository(AbstractRepository):
    def __init__(self, *args):
        self._books: List[Book] = list()
        self._authors: List[Author] = list()

        for book in args:
            self._books.append(book)
            for author in book.authors:
                self._authors.append(author)

        self.__users = list()
        self.__reviews = list()

    # def __iter__(self):
    #     self._current = 0
    #     return self
    #
    # def __next__(self):
    #     if self._current >= len(self._books):
    #         raise StopIteration
    #     else:
    #         self._current += 1
    #         return self._books[self._current - 1]

    def __len__(self):
        return len(self._books)

    def __getitem__(self, item):
        return self._books[item]

    # Function for testing purposes
    def get_books(self):
        return self._books

    def get_number_of_books(self):
        return len(self._books)

    # Book functions
    def add_book(self, book: Book):
        self._books.append(book)

    def get_book_by_id(self, id: int):
        books_list = [book for book in self._books if book.book_id == id]
        if books_list == []:
            return None
        return books_list

    def get_book_by_title(self, title: str):
        books_list = [book for book in self._books if book.title == title]
        if books_list == []:
            return None
        return books_list

    def get_book_by_author(self, author_name: str):
        books_list = []
        for book in self._books:
            for author in book.authors:
                if author.full_name == author_name:
                    books_list.append(book)
        if books_list == []:
            return None
        return books_list

    def get_book_by_publisher(self, publisher_name: str):
        books_list = [book for book in self._books if book.publisher.name == publisher_name]
        if books_list == []:
            return None
        return books_list

    def get_book_by_release_year(self, year: int):
        books_list = [book for book in self._books if book.release_year == year]
        if books_list == []:
            return None
        return books_list

    # User functions
    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def get_reviews(self):
        return self.__reviews

    def add_review(self, review: Review):
        super().add_review(review)
        self.__reviews.append(review)

    # def add_author(self, author: Author):
    #     super().add_author(author)
    #     self._authors.append(author)

    def add_author(self, author:Author):
        super()
        self._authors.append(author)
