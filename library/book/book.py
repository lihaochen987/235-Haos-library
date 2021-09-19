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
        'listbooks/list_books.html',
        books=repo.repo_instance,
        find_book_by_id_url=url_for('book_bp.find_book_by_id'),
        find_book_by_author_url=url_for('book_bp.find_book_by_author'),
        list_books_url=url_for('book_bp.list_books')
    )
    pass

@book_blueprint.route('/find_by_id', methods=['GET', 'POST'])
def find_book_by_id():
    form = IdSearchForm()

    if form.validate_on_submit():
        return render_template(
            'findbook/display_books.html',
            books=services.get_book_by_id(form.book_id.data, repo.repo_instance)
        )
    else:
        return render_template(
            'findbook/find_book_by_id.html',
            form=form,
            find_book_by_id_url=url_for('book_bp.find_book_by_id'),
            find_book_by_author_url=url_for('book_bp.find_book_by_author'),
            list_books_url=url_for('book_bp.list_books'),
            handler_url=url_for('book_bp.find_book_by_id')
        )

@book_blueprint.route('/find_by_author', methods=['GET', 'POST'])
def find_book_by_author():
    form = AuthorSearchForm()

    if form.validate_on_submit():
        return render_template(
            'findbook/display_books.html',
            books=services.get_book_by_author(form.book_author.data, repo.repo_instance)
        )
    else:
        return render_template(
            'findbook/find_book_by_author.html',
            form=form,
            find_book_by_id_url=url_for('book_bp.find_book_by_id'),
            find_book_by_author_url = url_for('book_bp.find_book_by_author'),
            list_books_url=url_for('book_bp.list_books'),
            handler_url=url_for('book_bp.find_book_by_author')
        )


class IdSearchForm(FlaskForm):
    book_id = IntegerField("Book id", [DataRequired()])
    submit = SubmitField("Find by Id")

class AuthorSearchForm(FlaskForm):
    book_author = StringField("Book author", [DataRequired()])
    submit = SubmitField("Find by Author")