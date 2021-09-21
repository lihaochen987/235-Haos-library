from flask import Blueprint, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired

import library.book.services as services
import library.adapters.repository as repo

book_blueprint = Blueprint(
    'book_bp', __name__
)

@book_blueprint.route('/list')
def list_books():
    return render_template(
        'book/listbooks.html',
        find_book_url=url_for('findbook_bp.find_book'),
        books=repo.repo_instance
    )
    pass