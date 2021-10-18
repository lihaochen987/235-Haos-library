from sqlalchemy import select, inspect

from library.adapters.orm import metadata
import sys

def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['authors', 'books', 'books_authors', 'publishers', 'reviews', 'users'] or ['authors','books','books_authors','books_publishers','publisher_book','publishers','reviews','users']

def test_database_populate_select_all_publishers(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    index = inspector.get_table_names().index("publishers")
    name_of_publishers_table = inspector.get_table_names()[index]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_publishers_table]])
        result = connection.execute(select_statement)

        all_publishers = []
        for row in result:
            all_publishers.append((row['id'], row['name']))

        assert len(all_publishers) == 46
        assert all_publishers[0] == (1, 'N/A')

def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    index = inspector.get_table_names().index("users")
    name_of_users_table = inspector.get_table_names()[index]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == ['thorke', 'fmercury', 'mjackson']

def test_database_populate_select_all_reviews(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    index = inspector.get_table_names().index("reviews")
    name_of_reviews_table = inspector.get_table_names()[index]


    with database_engine.connect() as connection:
        # query for records in table comments
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            all_reviews.append((row['id'], row['user_id'], row['book_id'], row['review_text']))

        assert all_reviews == [(1, 2, 707611, 'I loved reading this book!'), (2, 1, 12349665, "Didn't really like this one")]

def test_database_populate_select_all_books(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    index = inspector.get_table_names().index("books")
    name_of_books_table = inspector.get_table_names()[index]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_books_table]])
        result = connection.execute(select_statement)

        all_books = []
        for row in result:
            all_books.append((row['id'], row['title']))

        nr_books = len(all_books)
        assert nr_books == 46

        assert all_books[0] == (89371, 'The Te Of Piglet')


