from pathlib import Path

from library.adapters.repository import AbstractRepository
from library.adapters.csv_data_importer import load_books_authors_and_publishers, load_users, load_reviews


def populate(data_path: Path, repo: AbstractRepository,database_mode: bool):
    # Load books into the repository.
    load_books_authors_and_publishers(data_path, repo, database_mode)

    # Load users into the repository.
    users = load_users(data_path, repo)

    load_reviews(data_path, repo, users)
