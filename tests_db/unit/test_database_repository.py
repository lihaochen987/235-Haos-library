from datetime import date, datetime

import pytest

import library.adapters.repository as repo
from library.adapters.database_repository import SqlAlchemyRepository
from library.domain.model import User, Book, Author, Review, leave_review, Publisher
from library.adapters.repository import RepositoryException

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('dave')

    assert user2 == user and user2 is user

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None

def test_repository_can_retrieve_book_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_books = repo.get_number_of_books()

    # Check that the query returned 45 Articles.
    assert number_of_books == 45

def test_repository_can_add_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    publisher = Publisher("Testing")

    number_of_books = repo.get_number_of_books()

    new_book_id = number_of_books + 1
    book = Book(
        new_book_id,
        'Testing Book'
    )
    book.image_url = 'https://images.unsplash.com/photo-1624644128945-920c0da6931b?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80'
    book.ebook = False
    book.publisher = publisher

    repo.add_book(book)

    assert repo.get_book_by_id(new_book_id)[0] == book

def test_repository_can_retrieve_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = repo.get_book_by_id(12349665)

    # Check that the Book has the expected title attributes
    assert book[0].title == "Naoki Urasawa's 20th Century Boys, Volume 20 (20th Century Boys, #20)"
    assert book[0].release_year == 2012

    # assert book[0].authors == []
    # assert book[0].publisher == 'N/A'

    # Check that the Book is reviewed as expected.
    review_one = book[0].reviews[0]

    assert review_one.user.user_name == 'thorke'
    assert review_one.rating == 2

#
def test_repository_does_not_retrieve_a_non_existent_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = repo.get_book_by_id(3984573987459)
    assert book == []

def test_repository_can_retrieve_books_by_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_book_by_id(11827783)

    # Check that the query returned 1 Book.
    assert len(books) == 1
    assert books[0].book_id ==  11827783

    books = repo.get_book_by_id(17405342)
    assert books[0].book_id ==  17405342

    # Check that the query returned 1 Book.
    assert len(books) == 1

def test_repository_can_retrieve_books_by_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_book_by_title("The Switchblade Mamma")

    # Check that the query returned 1 Book.
    assert len(books) == 1
    assert books[0].title == "The Switchblade Mamma"

    books = repo.get_book_by_title("D.Gray-man, Vol. 16: Blood & Chains")

    # Check that the query returned 1 Book.
    assert len(books) == 1
    assert books[0].title == "D.Gray-man, Vol. 16: Blood & Chains"

def test_repository_does_not_retrieve_a_book_when_there_are_no_books_for_a_given_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_book_by_title("This title doesn't exist!")
    assert len(books) == 0

# def test_repository_can_retrieve_books_by_publisher(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     books = repo.get_book_by_publisher("Avatar Press")
#
#     # Check that the query returned 1 Book.
#     assert len(books) == 1
#     assert books[0].title == "The Switchblade Mamma"
#
#     books = repo.get_book_by_title("D.Gray-man, Vol. 16: Blood & Chains")
#
#     # Check that the query returned 1 Book.
#     assert len(books) == 1
#     assert books[0].title == "D.Gray-man, Vol. 16: Blood & Chains"

# def test_repository_does_not_retrieve_a_book_when_there_are_no_books_for_a_given_publisher(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     books = repo.get_book_by_title("This title doesn't exist!")
#     assert len(books) == 0

# def test_repository_can_retrieve_books_by_author(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     books = repo.get_book_by_author("Lindsey Schussman")

    # # Check that the query returned 1 Book.
    # assert len(books) == 1
    # assert books[0].title == "The Switchblade Mamma"
    #
    # books = repo.get_book_by_title("D.Gray-man, Vol. 16: Blood & Chains")
    #
    # # Check that the query returned 1 Book.
    # assert len(books) == 1
    # assert books[0].title == "D.Gray-man, Vol. 16: Blood & Chains"

# def test_repository_can_retrieve_tags(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     tags = repo.get_tags()
#
#     assert len(tags) == 10
#
#     tag_one = [tag for tag in tags if tag.tag_name == 'New Zealand'][0]
#     tag_two = [tag for tag in tags if tag.tag_name == 'Health'][0]
#     tag_three = [tag for tag in tags if tag.tag_name == 'World'][0]
#     tag_four = [tag for tag in tags if tag.tag_name == 'Politics'][0]
#
#     assert tag_one.number_of_tagged_articles == 53
#     assert tag_two.number_of_tagged_articles == 2
#     assert tag_three.number_of_tagged_articles == 64
#     assert tag_four.number_of_tagged_articles == 1
#
# def test_repository_can_get_first_article(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     article = repo.get_first_article()
#     assert article.title == 'Coronavirus: First case of virus in New Zealand'
#
# def test_repository_can_get_last_article(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     article = repo.get_last_article()
#     assert article.title == 'Covid 19 coronavirus: Kiwi mum on the heartbreak of losing her baby in lockdown'
#
# def test_repository_can_get_articles_by_ids(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     articles = repo.get_articles_by_id([2, 5, 6])
#
#     assert len(articles) == 3
#     assert articles[
#                0].title == 'Covid 19 coronavirus: US deaths double in two days, Trump says quarantine not necessary'
#     assert articles[1].title == "Australia's first coronavirus fatality as man dies in Perth"
#     assert articles[2].title == 'Coronavirus: Death confirmed as six more test positive in NSW'
#
# def test_repository_does_not_retrieve_article_for_non_existent_id(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     articles = repo.get_articles_by_id([2, 209])
#
#     assert len(articles) == 1
#     assert articles[
#                0].title == 'Covid 19 coronavirus: US deaths double in two days, Trump says quarantine not necessary'
#
# def test_repository_returns_an_empty_list_for_non_existent_ids(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     articles = repo.get_articles_by_id([0, 199])
#
#     assert len(articles) == 0
#
# def test_repository_returns_article_ids_for_existing_tag(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     article_ids = repo.get_article_ids_for_tag('Health')
#
#     assert article_ids == [1, 2]
#
# def test_repository_returns_an_empty_list_for_non_existent_tag(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     article_ids = repo.get_article_ids_for_tag('United States')
#
#     assert len(article_ids) == 0
#
#
# def test_repository_returns_date_of_previous_article(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     article = repo.get_article(6)
#     previous_date = repo.get_date_of_previous_article(article)
#
#     assert previous_date.isoformat() == '2020-03-01'
#
#
# def test_repository_returns_none_when_there_are_no_previous_articles(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     article = repo.get_article(1)
#     previous_date = repo.get_date_of_previous_article(article)
#
#     assert previous_date is None
#
#
# def test_repository_returns_date_of_next_article(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     article = repo.get_article(3)
#     next_date = repo.get_date_of_next_article(article)
#
#     assert next_date.isoformat() == '2020-03-05'
#
#
# def test_repository_returns_none_when_there_are_no_subsequent_articles(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     article = repo.get_article(177)
#     next_date = repo.get_date_of_next_article(article)
#
#     assert next_date is None
#
#
# def test_repository_can_add_a_tag(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     tag = Tag('Motoring')
#     repo.add_tag(tag)
#
#     assert tag in repo.get_tags()
#
#
# def test_repository_can_add_a_comment(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     user = repo.get_user('thorke')
#     article = repo.get_article(2)
#     comment = make_comment("Trump's onto it!", user, article)
#
#     repo.add_comment(comment)
#
#     assert comment in repo.get_comments()
#
#
# def test_repository_does_not_add_a_comment_without_a_user(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     article = repo.get_article(2)
#     comment = Comment(None, article, "Trump's onto it!", datetime.today())
#
#     with pytest.raises(RepositoryException):
#         repo.add_comment(comment)
#
#
# def test_repository_can_retrieve_comments(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     assert len(repo.get_comments()) == 3
#
#
# def make_article(new_article_date):
#     article = Article(
#         new_article_date,
#         'Coronavirus travel restrictions: Self-isolation deadline pushed back to give airlines breathing room',
#         'The self-isolation deadline has been pushed back',
#         'https://www.nzherald.co.nz/business/news/article.cfm?c_id=3&objectid=12316800',
#         'https://th.bing.com/th/id/OIP.0lCxLKfDnOyswQCF9rcv7AHaCz?w=344&h=132&c=7&o=5&pid=1.7'
#     )
#     return article
#
# def test_can_retrieve_an_article_and_add_a_comment_to_it(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     # Fetch Article and User.
#     article = repo.get_article(5)
#     author = repo.get_user('thorke')
#
#     # Create a new Comment, connecting it to the Article and User.
#     comment = make_comment('First death in Australia', author, article)
#
#     article_fetched = repo.get_article(5)
#     author_fetched = repo.get_user('thorke')
#
#     assert comment in article_fetched.comments
#     assert comment in author_fetched.comments
#
