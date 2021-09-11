from typing import List, Iterable

from library.adapters.repository import AbstractRepository
from library.domain.model import leave_review, Review, Book


class NonExistentBookException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(book_id: int, review_rating: int, comment_text: str, user_name: str, repo: AbstractRepository):
    # Check that Book exists.
    book = repo.get_book_by_id(book_id)
    if book is None:
        raise NonExistentBookException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    # Create Review
    review = leave_review(comment_text, review_rating, user, book)

    # Update the repository
    repo.add_review(review)


def get_reviews_for_book(book_id: int, repo: AbstractRepository):
    book = repo.get_book_by_id(book_id)

    if book is None:
        raise NonExistentBookException

    return reviews_to_dict(book.reviews)


# ============================================
# Functions to convert model entities to dicts
# ============================================

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
