from library.adapters.repository import AbstractRepository
from library.adapters.jsondatareader import BooksJSONReader
from typing import List
from library.domain.model import Book, User, Review, Author
from pathlib import Path


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

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self):
        if self._current >= len(self._books):
            raise StopIteration
        else:
            self._current += 1
            return self._books[self._current - 1]

    # Function for testing purposes
    def get_books(self):
        return self._books

    # Book functions
    def add_book(self, book: Book):
        self._books.append(book)

    def get_book_by_id(self, id: int):
        return next((book for book in self._books if book.book_id == id), None)

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

    def get_book_by_ebook_status(self, e_book_status: bool):
        books_list = [book for book in self._books if book.ebook == e_book_status]
        if books_list == []:
            return None
        return books_list

    def get_book_by_number_of_pages(self, pages: int):
        books_list = [book for book in self._books if book.num_pages == pages]
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


# Populate repo

def load_books(data_path: Path, repo: MemoryRepository):
    books_filename = str(data_path / "comic_books_excerpt.json")
    authors_filename = str(data_path / "book_authors_excerpt.json")
    reader = BooksJSONReader(books_filename, authors_filename)
    reader.read_json_files()
    return reader.dataset_of_books

def populate(data_path: Path, repo: MemoryRepository):
    books = load_books(data_path, repo)
    for book in books:
        repo.add_book(book)