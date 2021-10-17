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

        assert all_publishers == [(1, 'N/A'),
 (2, 'Dargaud'),
 (3, 'Hachette Partworks Ltd.'),
 (4, 'N/A'),
 (5, 'DC Comics'),
 (6, 'Go! Comi'),
 (7, 'Avatar Press'),
 (8, 'Avatar Press'),
 (9, 'Avatar Press'),
 (10, 'Avatar Press'),
 (11, 'N/A'),
 (12, 'Dynamite Entertainment'),
 (13, 'VIZ Media'),
 (14, 'Planeta DeAgostini'),
 (15, 'VIZ Media'),
 (16, 'N/A'),
 (17, 'Hakusensha'),
 (18, 'Shi Bao Wen Hua Chu Ban Qi Ye Gu Fen You Xian Gong Si'),
 (19, 'Marvel'),
 (20, 'N/A'),
 (21, "St. Martin's Press"),
 (22, 'Simon & Schuster Audio'),
 (23, 'Nelson Doubleday, Inc.'),
 (24, 'Atria Books'),
 (25, 'N/A'),
 (26, "Yesterday's Classics"),
 (27, 'Berkley Publishing Group'),
 (28, 'Seven Seas'),
 (29, 'Seven Seas'),
 (30, 'Gone Writing Publishing'),
 (31, 'Feral House'),
 (32, 'Simon & Schuster UK'),
 (33, 'N/A'),
 (34, 'N/A'),
 (35, 'Baumhaus Verlag GmbH'),
 (36, 'N/A'),
 (37, 'N/A'),
 (38, 'N/A'),
 (39, 'Random House Books for Young Readers'),
 (40, 'Blue Sky Press'),
 (41, 'Covenant Communications'),
 (42, 'N/A'),
 (43, 'Quinteto'),
 (44, 'N/A'),
 (45, 'Penguin Audio'),
 (46, 'N/A')]

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


