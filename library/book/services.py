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
    review = leave_review(comment_text,review_rating, user, book)

    # Update the repository
    repo.add_review(review)