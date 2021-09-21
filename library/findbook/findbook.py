from flask import Blueprint, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired

import library.findbook.services as services
import library.adapters.repository as repo

findbook_blueprint = Blueprint(
    'findbook_bp', __name__
)


# Initialisation functions
def initialise_forms():
    return IdSearchForm(), AuthorSearchForm(), PublisherSearchForm(), ReleaseYearSearchForm(), TitleSearchForm()


def render_page(id_form, author_form, publisher_form, release_form, title_form):
    return render_template(
        'findbook/findbook.html',
        id_form=id_form,
        author_form=author_form,
        publisher_form=publisher_form,
        release_form=release_form,
        title_form=title_form,
        find_book_url=url_for('findbook_bp.find_book'),
    )


@findbook_blueprint.route('/find_book', methods=['GET', 'POST'])
def find_book():
    id_form, author_form, publisher_form, release_form, title_form = initialise_forms()
    # id_form = IdSearchForm()
    # author_form = AuthorSearchForm()
    return render_page(id_form, author_form, publisher_form, release_form, title_form)


@findbook_blueprint.route('/find_book_by_id', methods=['GET', 'POST'])
def find_book_by_id():
    id_form, author_form, publisher_form, release_form, title_form = initialise_forms()

    if id_form.validate_on_submit():
        if (services.get_book_by_id(id_form.book_id.data, repo.repo_instance) == None):
            return render_page(id_form, author_form, publisher_form, release_form, title_form)
        else:
            return render_template(
                'findbook/displaybooks.html',
                books=services.get_book_by_id(id_form.book_id.data, repo.repo_instance),
            )
    else:
        return render_page(id_form, author_form, publisher_form, release_form, title_form)


@findbook_blueprint.route('/find_book_by_title', methods=['GET', 'POST'])
def find_book_by_title():
    id_form, author_form, publisher_form, release_form, title_form = initialise_forms()

    if title_form.validate_on_submit():
        if (services.get_book_by_title(title_form.book_title.data, repo.repo_instance) == None):
            return render_page(id_form, author_form, publisher_form, release_form, title_form)
        else:
            return render_template(
                'findbook/displaybooks.html',
                books=services.get_book_by_title(title_form.book_title.data, repo.repo_instance),
            )
    else:
        return render_page(id_form, author_form, publisher_form, release_form, title_form)


@findbook_blueprint.route('/find_book_by_author', methods=['GET', 'POST'])
def find_book_by_author():
    id_form, author_form, publisher_form, release_form, title_form = initialise_forms()

    if author_form.validate_on_submit():
        if (services.get_book_by_author(author_form.book_author.data, repo.repo_instance) == None):
            return render_page(id_form, author_form, publisher_form, release_form, title_form)
        else:
            return render_template(
                'findbook/displaybooks.html',
                books=services.get_book_by_author(author_form.book_author.data, repo.repo_instance),
            )
    else:
        return render_page(id_form, author_form, publisher_form, release_form, title_form)


@findbook_blueprint.route('/find_book_by_publisher', methods=['GET', 'POST'])
def find_book_by_publisher():
    id_form, author_form, publisher_form, release_form, title_form = initialise_forms()

    if publisher_form.validate_on_submit():
        if (services.get_book_by_publisher(publisher_form.book_publisher.data, repo.repo_instance) == None):
            return render_page(id_form, author_form, publisher_form, release_form, title_form)
        else:
            return render_template(
                'findbook/displaybooks.html',
                books=services.get_book_by_publisher(publisher_form.book_publisher.data, repo.repo_instance),
            )
    else:
        return render_page(id_form, author_form, publisher_form, release_form, title_form)


@findbook_blueprint.route('/find_book_by_release_year', methods=['GET', 'POST'])
def find_book_by_release_year():
    id_form, author_form, publisher_form, release_form, title_form = initialise_forms()

    if release_form.validate_on_submit():
        if (services.get_book_by_release_year(release_form.book_year.data, repo.repo_instance) == None):
            return render_page(id_form, author_form, release_form, release_form, title_form)
        else:
            return render_template(
                'findbook/displaybooks.html',
                books=services.get_book_by_release_year(release_form.book_year.data, repo.repo_instance),
            )
    else:
        return render_page(id_form, author_form, publisher_form, release_form, title_form)


class IdSearchForm(FlaskForm):
    book_id = IntegerField("Book id", [DataRequired()])
    submit = SubmitField("Find by Id")


class AuthorSearchForm(FlaskForm):
    book_author = StringField("Book author", [DataRequired()])
    submit = SubmitField("Find by Author Name")


class PublisherSearchForm(FlaskForm):
    book_publisher = StringField("Book publisher", [DataRequired()])
    submit = SubmitField("Find by Publisher")


class ReleaseYearSearchForm(FlaskForm):
    book_year = IntegerField("Book release year", [DataRequired()])
    submit = SubmitField("Find by Release Year")


class EbookSearchForm(FlaskForm):
    book_ebook = IntegerField("Book ebook status", [DataRequired()])
    submit = SubmitField("Find by ebook status")


class TitleSearchForm(FlaskForm):
    book_title = StringField("Book title", [DataRequired()])
    submit = SubmitField("Find by Book Title")
