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
    assert str(book_services.get_book_by_id(834987324897934759, in_memory_repo)) == 'None'
    assert str(book_services.get_book_by_id(11827783,
                                            in_memory_repo)) == '<Book Sherlock Holmes: Year One, book id = 11827783>'


def test_can_get_book_by_author(in_memory_repo):
    assert str(book_services.get_book_by_title('HaoChen Li', in_memory_repo)) == 'None'
    assert str(book_services.get_book_by_title('Sherlock Holmes: Year One',
                                               in_memory_repo)) == '[<Book Sherlock Holmes: Year One, book id = 11827783>]'


def test_can_get_book_by_publisher(in_memory_repo):
    assert str(book_services.get_book_by_publisher('HaoChen Li', in_memory_repo)) == 'None'
    assert str(book_services.get_book_by_publisher('Dynamite Entertainment',
                                                   in_memory_repo)) == '[<Book Sherlock Holmes: Year One, book id = 11827783>]'


def test_can_get_book_by_release_year(in_memory_repo):
    assert str(book_services.get_book_by_release_year(273648237, in_memory_repo)) == 'None'
    assert str(book_services.get_book_by_release_year(2011,
                                                      in_memory_repo)) == '[<Book Sherlock Holmes: Year One, book id = 11827783>, <Book 續．星守犬, book id = 18711343>]'


def test_can_get_book_by_ebook_status(in_memory_repo):
    assert str(book_services.get_book_by_ebook_status(True,
                                                      in_memory_repo)) == '[<Book The Switchblade Mamma, book id = 25742454>, <Book Bounty Hunter 4/3: My Life in Combat from Marine Scout Sniper to MARSOC, book id = 35452242>, <Book She Wolf #1, book id = 30735315>, <Book D.Gray-man, Vol. 16: Blood & Chains, book id = 18955715>]'


def test_can_get_book_by_number_of_pages(in_memory_repo):
    assert str(book_services.get_book_by_number_of_pages(144, in_memory_repo)) == '[<Book War Stories, Volume 4, book id = 27036539>, <Book Sherlock Holmes: Year One, book id = 11827783>]'
    assert str(book_services.get_book_by_number_of_pages(27836478236, in_memory_repo)) == 'None'
