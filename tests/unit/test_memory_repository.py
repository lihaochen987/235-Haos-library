from datetime import date, datetime
from typing import List

import pytest

from library.domain.model import Book, Author, Publisher, User
from library.domain.model import leave_review

from library.adapters.repository import RepositoryException


# Testing for the book class
@pytest.fixture()
def book():
    some_book = Book(1, "Harry Potter and the Chamber of Secrets")
    some_author = Author(52, "J. K. Rowling")
    some_publisher = Publisher("Bloomsbury Publishing")
    some_book.description = "Ever since Harry Potter had come home for the summer, the Dursleys had been so mean \
                         and hideous that all Harry wanted was to get back to the Hogwarts School for \
                         Witchcraft and Wizardry. But just as he’s packing his bags, Harry receives a \
                         warning from a strange impish creature who says that if Harry returns to Hogwarts, \
                         disaster will strike."
    some_book.release_year = 1999
    some_book.num_pages = 500
    some_book.ebook = True

    some_book.add_author(some_author)
    some_book.publisher = some_publisher
    return some_book


def test_repository_can_get_book_by_id(in_memory_repo, book):
    in_memory_repo.add_book(book)

    assert in_memory_repo.get_book_by_id(1)[0] is book


def test_repository_does_not_retrieve_a_non_existent_id(in_memory_repo):
    book = in_memory_repo.get_book_by_id(378434)
    assert book is None


def test_repository_can_get_book_by_title(in_memory_repo, book):
    in_memory_repo.add_book(book)

    assert in_memory_repo.get_book_by_title("Harry Potter and the Chamber of Secrets")[0] is book


def test_repository_does_not_retrieve_a_non_existent_title(in_memory_repo):
    book = in_memory_repo.get_book_by_title("uiasydiuasyuidsahiodsa")
    assert book is None


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


def test_repository_does_not_retrieve_a_non_existent_author(in_memory_repo):
    book = in_memory_repo.get_book_by_author("uiasydiuasyuidsahiodsa")
    assert book is None


def test_repository_can_get_book_by_publisher(in_memory_repo, book):
    in_memory_repo.add_book(book)

    assert in_memory_repo.get_book_by_publisher("Bloomsbury Publishing")[0] is book


def test_repository_can_get_multiple_books_by_same_publisher(in_memory_repo, book):
    in_memory_repo.add_book(book)

    another_book = Book(32, "Harry Potter and the Philosopher's Stone")
    another_publisher = Publisher("Bloomsbury Publishing")
    another_book.publisher = another_publisher
    in_memory_repo.add_book(another_book)

    assert in_memory_repo.get_book_by_publisher("Bloomsbury Publishing")[0] is book
    assert in_memory_repo.get_book_by_publisher("Bloomsbury Publishing")[1] is another_book
    assert len(in_memory_repo.get_book_by_publisher("Bloomsbury Publishing")) == 2


def test_repository_does_not_retrieve_a_non_existent_publisher(in_memory_repo):
    book = in_memory_repo.get_book_by_publisher("uiasydiuasyuidsahiodsa")
    assert book is None


def test_repository_can_get_book_by_release_year(in_memory_repo, book):
    in_memory_repo.add_book(book)

    assert in_memory_repo.get_book_by_release_year(1999)[0] is book


def test_repository_can_get_multiple_books_by_release_year(in_memory_repo, book):
    in_memory_repo.add_book(book)

    another_book = Book(23, "The Reptile Room")
    another_book.release_year = 1999
    in_memory_repo.add_book(another_book)

    some_book = Book(32, "Harry Potter and the Philosopher's Stone")
    some_book.release_year = 1997
    in_memory_repo.add_book(some_book)

    assert in_memory_repo.get_book_by_release_year(1999)[0] is book
    assert in_memory_repo.get_book_by_release_year(1999)[1] is another_book
    assert len(in_memory_repo.get_book_by_release_year(1999)) == 2


def test_repository_does_not_retrieve_a_non_existent_release_year(in_memory_repo):
    book = in_memory_repo.get_book_by_author(4857949)
    assert book is None


# def test_repository_can_get_book_by_e_book_status(in_memory_repo, book):
#     in_memory_repo.add_book(book)
#
#     assert in_memory_repo.get_book_by_ebook_status(True)[-1] is book
#
#
# def test_repository_can_get_multiple_books_by_e_book_status(in_memory_repo, book):
#     in_memory_repo.add_book(book)
#     assert in_memory_repo.get_book_by_ebook_status(True)[-1] is book
#
#     another_book = Book(23, "The Reptile Room")
#     another_book.ebook = True
#     in_memory_repo.add_book(another_book)
#
#     assert in_memory_repo.get_book_by_ebook_status(True)[-1] is another_book
#
#     some_book = Book(32, "Harry Potter and the Philosopher's Stone")
#     some_book.ebook = False
#     in_memory_repo.add_book(some_book)
#
#     assert in_memory_repo.get_book_by_ebook_status(False)[-1] is some_book


# def test_repository_can_get_book_by_number_of_pages(in_memory_repo, book):
#     in_memory_repo.add_book(book)
#
#     assert in_memory_repo.get_book_by_number_of_pages(500)[0] is book


# def test_repository_can_get_multiple_books_by_number_of_pages(in_memory_repo, book):
#     in_memory_repo.add_book(book)
#
#     another_book = Book(23, "The Reptile Room")
#     another_book.num_pages = 500
#     in_memory_repo.add_book(another_book)
#
#     some_book = Book(32, "Harry Potter and the Philosopher's Stone")
#     some_book.num_pages = 350
#     in_memory_repo.add_book(some_book)
#
#     assert in_memory_repo.get_book_by_number_of_pages(500)[0] is book
#     assert in_memory_repo.get_book_by_number_of_pages(500)[1] is another_book
#     assert in_memory_repo.get_book_by_number_of_pages(350)[0] is some_book
#     assert len(in_memory_repo.get_book_by_number_of_pages(500)) == 2
#     assert len(in_memory_repo.get_book_by_number_of_pages(350)) == 1
#
#
# def test_repository_does_not_retrieve_a_non_existent_number_of_pages(in_memory_repo):
#     book = in_memory_repo.get_book_by_number_of_pages(28937498723984)
#     assert book is None


# Testing for the User class
@pytest.fixture()
def user():
    user = User('hli779', 'Somepassword123')
    return user


def test_repository_can_add_a_user(in_memory_repo):
    user = User('dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    in_memory_repo.add_user(User('fmercury', '8734gfe2058v'))
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_add_and_retrieve_reviews(in_memory_repo, user, book):
    in_memory_repo.add_user(user)
    in_memory_repo.add_book(book)

    review = leave_review("Trump's onto it!", 5, user, book)
    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews()
    assert len(in_memory_repo.get_reviews()) == 1


def test_repository_can_populate(in_memory_repo):
    assert len(in_memory_repo.get_books()) == 20

def test_repository_populate_books_are_linked_with_authors(in_memory_repo):
    book = in_memory_repo.get_book_by_id(18955715)[0]
    assert str(book.authors) == '[<Author Katsura Hoshino, author id = 311098>]'
