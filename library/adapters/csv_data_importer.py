import csv
from pathlib import Path
from datetime import date, datetime

from werkzeug.security import generate_password_hash

from library.adapters.repository import AbstractRepository
from library.adapters.jsondatareader import BooksJSONReader
from library.domain.model import Book, Author, Review, User, leave_review, ModelException


# Populate repo
def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row

def load_books(data_path: Path, repo: AbstractRepository):
    books_filename = str(Path(data_path) / "comic_books_excerpt.json")
    authors_filename = str(Path(data_path) / "book_authors_excerpt.json")
    reader = BooksJSONReader(books_filename, authors_filename)
    reader.read_json_files()
    for book in reader.dataset_of_books:
        repo.add_book(book)

def load_users(data_path:Path, repo:AbstractRepository):
    users = dict()

    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users

def load_reviews(data_path: Path, repo: AbstractRepository, users):
    reviews_filename = str(Path(data_path) / "reviews.csv")
    for data_row in read_csv_file(reviews_filename):
        review = leave_review(
            review_text = data_row[0],
            user=users[data_row[2]],
            book = repo.get_book_by_id(int(data_row[3]))[0],
            review_rating = int(data_row[1]),
        )
        repo.add_review(review)

def populate(data_path: Path, repo: AbstractRepository):
    load_books(data_path, repo)
    users = load_users(data_path, repo)