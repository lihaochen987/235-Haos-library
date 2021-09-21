from typing import List, Iterable

from library.adapters.repository import AbstractRepository
from library.domain.model import leave_review, Review, Book, Author


class NonExistentBookException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_book_by_id(book_id: int, repo: AbstractRepository):
    books = repo.get_book_by_id(book_id)
    if books == None:
        return None
    return books


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

def add_review(book_id: int, review_rating: int, comment_text: str, user_name: str, repo: AbstractRepository):
    # Check that Book exists.
    books = repo.get_book_by_id(book_id)
    if len(books) == 0:
        raise NonExistentBookException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    # Create Review
    review = leave_review(comment_text, review_rating, user, books[0])

    # Update the repository
    repo.add_review(review)


def get_reviews_for_book(book_id: int, repo: AbstractRepository):
    book = repo.get_book_by_id(book_id)

    if len(book) == 0:
        raise NonExistentBookException

    return reviews_to_dict(book[0].reviews)


# ============================================
# Functions to convert model entities to dicts
# ============================================

def author_to_dict(author: Author):
    author_dict = {
        'unique_id': author.unique_id,
        'full_name': author.full_name
    }
    return author_dict


def authors_to_dict(authors: Iterable[Author]):
    return [author_to_dict(author) for author in authors]


def review_to_dict(review: Review):
    review_dict = {
        'user_name': review.user.user_name,
        'review_rating': review.rating,
        'book_id': review.book.book_id,
        'review_text': review.review_text,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]