from flask import Blueprint, render_template, url_for

import library.utilities.utilities as utilities


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/')
def home():
    return render_template(
        'home/home.html',
        find_book_by_id_url=url_for('book_bp.find_book_by_id'),
        find_book_by_author_url=url_for('book_bp.find_book_by_author'),
        list_books_url=url_for('book_bp.list_books')
    )