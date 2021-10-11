import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from library.domain.model import User, Publisher, Book, leave_review


# article_date = datetime.date(2020, 2, 28)


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_book(empty_session):
    publisher_id = 987654321
    # empty_session.execute('INSERT INTO publishers (id, publisher_name) VALUES (:id, "Houghton Mifflin Harcourt")', {'publisher_id':publisher_id})
    id = 123456789
    release_year = 2005
    num_pages = 1216
    ebook = True

    empty_session.execute(
        'INSERT INTO books (id, title, description, image_url, publisher, release_year, ebook, num_pages) VALUES '
        '(:id, '
        '"The Lord of the Rings", '
        '"In ancient times the Rings of Power were crafted by the Elven-smiths, and Sauron, the Dark Lord, forged the One Ring, filling it with his own power so that he could rule all others.", '
        '"https://images.unsplash.com/photo-1541963463532-d68292c34b19?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=688&q=80", '
        ':publisher,'
        ':release_year,'
        ':ebook,'
        ':num_pages)',
        {'id': id, 'publisher': publisher_id, 'release_year': release_year, 'num_pages': num_pages, 'ebook': ebook}
    )
    row = empty_session.execute('SELECT id from books').fetchone()
    return row[0]
#
#
# def insert_tags(empty_session):
#     empty_session.execute(
#         'INSERT INTO tags (tag_name) VALUES ("News"), ("New Zealand")'
#     )
#     rows = list(empty_session.execute('SELECT id from tags'))
#     keys = tuple(row[0] for row in rows)
#     return keys
#
#
# def insert_article_tag_associations(empty_session, article_key, tag_keys):
#     stmt = 'INSERT INTO article_tags (article_id, tag_id) VALUES (:article_id, :tag_id)'
#     for tag_key in tag_keys:
#         empty_session.execute(stmt, {'article_id': article_key, 'tag_id': tag_key})
#
#
def insert_reviewed_book(empty_session):
    book_key = insert_book(empty_session)
    user_key = insert_user(empty_session)
    rating = 4

    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        'INSERT INTO reviews (user_id, book_id, review_text, rating, timestamp) VALUES '
        '(:user_id, :book_id, "Review_text 1", :rating, :timestamp_1),'
        '(:user_id, :book_id, "Review_text 2", :rating, :timestamp_2)',
        {'user_id': user_key, 'book_id': book_key, 'rating':rating, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT id from books').fetchone()
    return row[0]
#
#
def make_book():
    book = Book(123456789, 'The Lord of the Rings')
    book.description = "In ancient times the Rings of Power were crafted by the Elven-smiths, and Sauron, the Dark Lord, forged the One Ring, filling it with his own power so that he could rule all others."
    book.image_url = "https://images.unsplash.com/photo-1541963463532-d68292c34b19?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=688&q=80"
    book.publisher = Publisher('Houghton Mifflin Harcourt')
    book.release_year = 2005
    book.ebook = True
    book.num_pages = 1216
    book.similar_books = [56789, 12345]
    return book


def make_user():
    user = User("Andrew", "11123456676575575")
    return user


# def make_tag():
#     tag = Tag("News")
#     return tag


def test_loading_of_users(empty_session):
    users = list()
    users.append(("andrew", "1234"))
    users.append(("cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("Andrew", "1234"),
        User("Cindy", "999")
    ]

    assert empty_session.query(User).all() == expected



def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("andrew", "11123456676575575")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("Andrew", "1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Andrew", "111")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_book(empty_session):
    book_key = insert_book(empty_session)
    expected_book = make_book()
    fetched_book = empty_session.query(Book).one()

    assert expected_book == fetched_book
    assert book_key == fetched_book.book_id


# def test_loading_of_tagged_article(empty_session):
#     article_key = insert_article(empty_session)
#     tag_keys = insert_tags(empty_session)
#     insert_article_tag_associations(empty_session, article_key, tag_keys)
#
#     article = empty_session.query(Article).get(article_key)
#     tags = [empty_session.query(Tag).get(key) for key in tag_keys]
#
#     for tag in tags:
#         assert article.is_tagged_by(tag)
#         assert tag.is_applied_to(article)


def test_loading_of_reviewed_book(empty_session):
    insert_reviewed_book(empty_session)

    rows = empty_session.query(Book).all()
    book = rows[0]

    for review in book.reviews:
        assert review.book is book

#
def test_saving_of_review(empty_session):
    book_key = insert_book(empty_session)
    user_key = insert_user(empty_session, ("Andrew", "1234"))

    rows = empty_session.query(Book).all()
    book = rows[0]
    user = empty_session.query(User).filter(User._User__user_name == "Andrew").one()

    # Create a new Review that is bidirectionally linked with the User and Book.
    review_text = "Some review text."
    review = leave_review(review_text, 5, user, book)

    # Note: if the bidirectional links between the new Review and the User and
    # Book objects hadn't been established in memory, they would exist following
    # committing the addition of the Review to the database.
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, book_id, review_text FROM reviews'))

    assert rows == [(user_key, book_key, review_text)]


def test_saving_of_book(empty_session):
    book = make_book()
    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute(
        'SELECT id, title, description, image_url, publisher, release_year, ebook, num_pages FROM books'))
    assert rows == [(123456789, 'The Lord of the Rings',
                     'In ancient times the Rings of Power were crafted by the Elven-smiths, and Sauron, the Dark Lord, forged the One Ring, filling it with his own power so that he could rule all others.',
                     'https://images.unsplash.com/photo-1541963463532-d68292c34b19?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=688&q=80',
                     None, 2005, 1, None)]


# def test_saving_tagged_article(empty_session):
#     article = make_article()
#     tag = make_tag()
#
#     # Establish the bidirectional relationship between the Article and the Tag.
#     make_tag_association(article, tag)
#
#     # Persist the Article (and Tag).
#     # Note: it doesn't matter whether we add the Tag or the Article. They are connected
#     # bidirectionally, so persisting either one will persist the other.
#     empty_session.add(article)
#     empty_session.commit()
#
#     # Test test_saving_of_article() checks for insertion into the articles table.
#     rows = list(empty_session.execute('SELECT id FROM articles'))
#     article_key = rows[0][0]
#
#     # Check that the tags table has a new record.
#     rows = list(empty_session.execute('SELECT id, tag_name FROM tags'))
#     tag_key = rows[0][0]
#     assert rows[0][1] == "News"
#
#     # Check that the article_tags table has a new record.
#     rows = list(empty_session.execute('SELECT article_id, tag_id from article_tags'))
#     article_foreign_key = rows[0][0]
#     tag_foreign_key = rows[0][1]
#
#     assert article_key == article_foreign_key
#     assert tag_key == tag_foreign_key


def test_save_review_book(empty_session):
    # Create Book User objects.
    book = make_book()
    user = make_user()

    # Create a new Comment that is bidirectionally linked with the User and Book.
    review_text = "Some review text."
    review = leave_review(review_text, 3, user, book)

    # Save the new Book.
    empty_session.add(book)
    empty_session.commit()

    # Test test_saving_of_book() checks for insertion into the books table.
    rows = list(empty_session.execute('SELECT id FROM books'))
    book_key = rows[0][0]

    # Test test_saving_of_users() checks for insertion into the users table.
    rows = list(empty_session.execute('SELECT id FROM users'))
    user_key = rows[0][0]

    # Check that the reviews table has a new record that links to the books and users
    # tables.
    rows = list(empty_session.execute('SELECT user_id, book_id, review_text FROM reviews'))
    assert rows == [(user_key, book_key, review_text)]
