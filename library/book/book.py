from flask import Blueprint, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired

import library.book.services as services
import library.adapters.memory_repository as repo

book_blueprint = Blueprint(
    'book_bp', __name__
)

@book_blueprint.route('/list')
def list_books():
    return render_template(
        'listbooks/list_books.html',
        books=repo.repo_instance,
        find_book_by_id_url=url_for('book_bp.find_book_by_id'),
        find_book_by_author_url=url_for('book_bp.find_book_by_author'),
        list_books_url=url_for('book_bp.list_books')
    )
    pass