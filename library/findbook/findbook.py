from better_profanity import profanity
from flask import Blueprint, render_template, url_for, request, session
from flask_paginate import Pagination, get_page_parameter
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, TextAreaField, validators
from wtforms.validators import DataRequired, Length

import library.adapters.repository as repo
import library.findbook.services as services
from library.authentication.authentication import login_required

findbook_blueprint = Blueprint(
    'findbook_bp', __name__
)


@findbook_blueprint.route('/list')
def list_books():
    form = ReviewForm()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    books = repo.repo_instance
    pagination = Pagination(page=page, total=len(books))
    return render_template(
        'findbook/displaybooks.html',
        find_book_url=url_for('findbook_bp.find_book'),
        books=repo.repo_instance,
        pagination=pagination,
        form=form
    )
    pass


@findbook_blueprint.route('/find_book', methods=['GET'])
def find_book():
    book_form = BookForm()
    return render_template('findbook/findbook.html', book_form=book_form, handler_url=url_for('findbook_bp.view_books'))


@findbook_blueprint.route('/view_books', methods=['GET', 'POST'])
def view_books():
    book_repo = repo.repo_instance
    book_form = BookForm()
    form = ReviewForm()
    print(book_form.errors)

    if book_form.is_submitted():
        print("submitted")

    if book_form.validate():
        print("valid")

    print(book_form.errors)
    if request.method == 'POST':
        if book_form.validate_on_submit():
            print(request.form)
            books = []
            for field in book_form:
                if (field.data != "" or field.data != None or field.data != True):
                    temp_books = check_and_return(field.name, book_form)
                    if temp_books == None:
                        pass
                    else:
                        for book in temp_books:
                            books.append(book)
            books = list(set(books))
            page = request.args.get(get_page_parameter(), type=int, default=1)
            pagination = Pagination(page=page, total=len(books))
            return render_template('findbook/displaybooks.html', books=books, pagination=pagination,
                                   book_form=book_form, form=form, handler_url=url_for('findbook_bp.add_review'))


@findbook_blueprint.route('/add_review', methods=['GET', 'POST'])
@login_required
def add_review():
    user_name = session['user_name']
    form = ReviewForm()
    book_id = int(request.values.get("book_id"))
    books = services.get_book_by_id(book_id, repo.repo_instance)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=len(books))
    services.add_review(book_id, 4, request.values.get("review"), user_name,
                        repo.repo_instance)
    return render_template('findbook/displaybooks.html', pagination=pagination,
                           books=books, form = form)

def check_and_return(field_name, book_form):
    if field_name == 'book_year':
        return services.get_book_by_release_year(book_form.book_year.data, repo.repo_instance)
    if field_name == "book_id":
        return services.get_book_by_id(book_form.book_id.data, repo.repo_instance)
    if field_name == "book_author":
        return services.get_book_by_author(book_form.book_author.data, repo.repo_instance)
    if field_name == "book_year":
        return services.get_book_by_release_year(book_form.book_year.data, repo.repo_instance)
    if field_name == "book_title":
        return services.get_book_by_title(book_form.book_title.data, repo.repo_instance)

# @findbook_blueprint.route('/review', methods=['GET', 'POST'])
# @login_required
# def add_review():
#     id_form, author_form, publisher_form, release_form, title_form = initialise_forms()
#
#     user_name = session['user_name']
#     review_form = ReviewForm()
#
#     if review_form.validate_on_submit():
#         # Successful POST, i.e. the comment text has passed data validation.
#         # Extract the article id, representing the commented article, from the form.
#         book_id = int(review_form.book_id.data)
#         print(book_id)
#
#         # Use the service layer to store the new comment.
#         services.add_review(book_id, 5, review_form.review, user_name, repo.repo_instance)
#
#         # Retrieve the article in dict form.
#         book = services.get_book_by_id(book_id, repo.repo_instance)
#
#         # Cause the web browser to display the page of all articles that have the same date as the commented article,
#         # and display all comments, including the new comment.
#         return redirect(url_for('findbook_bp.find_book_by_id', date=article['date'], view_comments_for=article_id))
#
#     if request.method == 'GET':
#         # Request is a HTTP GET to display the form.
#         # Extract the article id, representing the article to comment, from a query parameter of the GET request.
#         article_id = int(request.args.get('article'))
#
#         # Store the article id in the form.
#         form.article_id.data = article_id
#     else:
#         # Request is a HTTP POST where form validation has failed.
#         # Extract the article id of the article being commented from the form.
#         article_id = int(form.article_id.data)
#
#     # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
#     # the user to enter a comment. The generated Web page includes a form object.
#     article = services.get_article(article_id, repo.repo_instance)
#     return render_template(
#         'news/comment_on_article.html',
#         title='Edit article',
#         article=article,
#         form=form,
#         handler_url=url_for('news_bp.comment_on_article'),
#         selected_articles=utilities.get_selected_articles(),
#         tag_urls=utilities.get_tags_and_urls()
#     )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class BookForm(FlaskForm):
    book_id = IntegerField("Book id", [validators.optional()])
    book_author = StringField("Book author", [validators.optional()])
    book_publisher = StringField("Book publisher", [validators.optional()])
    book_year = IntegerField("Book release year", [validators.optional()])
    book_title = StringField("Book title", [validators.optional()])
    submit = SubmitField("Find Books", [validators.optional()])


class ReviewForm(BookForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    book_id = IntegerField("Book ID")
    submit = SubmitField('Submit Review')
