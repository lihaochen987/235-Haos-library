from flask import Blueprint, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired

import library.findbook.services as services
import library.adapters.repository as repo

findbook_blueprint = Blueprint(
    'findbook_bp', __name__
)


@findbook_blueprint.route('/find_book', methods=['GET', 'POST'])
def find_book():
    id_form = IdSearchForm()
    author_form = AuthorSearchForm()
    return render_template('findbook/findbook.html', id_form=id_form, author_form=author_form)


@findbook_blueprint.route('/find_book_by_id', methods=['GET', 'POST'] )
def find_book_by_id():
    id_form = IdSearchForm()
    author_form = AuthorSearchForm()

    if id_form.validate_on_submit():
        if (services.get_book_by_id(id_form.book_id.data, repo.repo_instance) == None):
            return render_template(
                'findbook/findbook.html',
                id_form=id_form,
                author_form = author_form,
                find_book_url=url_for('findbook_bp.find_book'),
                find_book_by_id_url=url_for('findbook_bp.find_book'),
                handler_url=url_for('findbook_bp.find_book')
            )
        else:
            return render_template(
                'findbook/displaybooks.html',
                books=services.get_book_by_id(id_form.book_id.data, repo.repo_instance),
                id_form = id_form,
                author_form = author_form
            )
    else:
        return render_template(
            'findbook/findbook.html',
            id_form=id_form,
            author_form = author_form,
            find_book_url=url_for('findbook_bp.find_book'),
            find_book_by_id_url=url_for('findbook_bp.find_book'),
            handler_url=url_for('findbook_bp.find_book')
        )


# @findbook_blueprint.route('/find_book', methods=['GET', 'POST'])
# def find_book():
#     id_form = IdSearchForm()
#
#     if id_form.validate_on_submit():
#         if (services.get_book_by_id(id_form.book_id.data, repo.repo_instance) == None):
#             return render_template(
#                 'findbook/findbook.html',
#                 id_form=id_form,
#                 find_book_url=url_for('findbook_bp.find_book'),
#                 find_book_by_id_url=url_for('findbook_bp.find_book'),
#                 handler_url=url_for('findbook_bp.find_book')
#             )
#         else:
#             return render_template(
#                 'findbook/displaybooks.html',
#                 books=services.get_book_by_id(id_form.book_id.data, repo.repo_instance)
#             )
#     else:
#         return render_template(
#             'findbook/findbook.html',
#             id_form=id_form,
#             find_book_url=url_for('findbook_bp.find_book'),
#             find_book_by_id_url=url_for('findbook_bp.find_book'),
#             handler_url=url_for('findbook_bp.find_book')
#         )


# @findbook_blueprint.route('/find_by_id', methods=['GET', 'POST'])
# def find_book_by_id():
#     form = IdSearchForm()
#
#     if form.validate_on_submit():
#         return render_template(
#             'findbook/displaybooks.html',
#             books=services.get_book_by_id(form.book_id.data, repo.repo_instance)
#         )
#     else:
#         return render_template(
#             'findbook/findbook.html',
#             form=form,
#             find_book_url=url_for('findbook_bp.find_book'),
#             find_book_by_id_url=url_for('findbook_bp.find_book_by_id'),
#             handler_url = url_for('findbook_bp.find_book_by_id')
#         )


#
# @findbook_blueprint.route('/find_by_author', methods=['GET', 'POST'])
# def find_book_by_author():
#     form = AuthorSearchForm()
#
#     if form.validate_on_submit():
#         return render_template(
#             'findbook/display_books.html',
#             books=services.get_book_by_author(form.book_author.data, repo.repo_instance)
#         )
#     else:
#         return render_template(
#             'findbook/find_book_by_author.html',
#             form=form,
#             find_book_by_id_url=url_for('book_bp.find_book_by_id'),
#             find_book_by_author_url = url_for('book_bp.find_book_by_author'),
#             list_books_url=url_for('book_bp.list_books'),
#             handler_url=url_for('book_bp.find_book_by_author')
#         )

class IdSearchForm(FlaskForm):
    book_id = IntegerField("Book id", [DataRequired()])
    submit = SubmitField("Find by Id")


class AuthorSearchForm(FlaskForm):
    book_author = StringField("Book author", [DataRequired()])
    submit = SubmitField("Find by Author")
