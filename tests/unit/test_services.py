from datetime import date

import pytest

from library.book import services as book_services

def test_can_add_review(in_memory_repo):
    book_id = 27036538
    review_rating = 5
    review_text = "Fantastic book, I was at the edge of my seat!"
    user_name = "fmercury"

    # Call the service layer to add the comment
    book_services.add_review(book_id, review_rating, review_text, user_name, in_memory_repo)

    # Retrieve the comments for the book from the repository
    reviews_as_dict = book_services.get_reviews_for_book(book_id, in_memory_repo)

    # Check that reviews include a review with the new review text
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text),
        None) is not None

def test_can_get_book_by_id(in_memory_repo):
    assert str(book_services.get_book_by_id(11827783, in_memory_repo)) == '<Book Sherlock Holmes: Year One, book id = 11827783>'
