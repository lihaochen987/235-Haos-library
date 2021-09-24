from collections import namedtuple

from better_profanity import profanity
from flask import Blueprint, render_template, url_for, request, session, redirect
from flask_paginate import Pagination, get_page_parameter, get_page_args
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, TextAreaField, validators
from wtforms.validators import DataRequired, Length, ValidationError

import library.adapters.repository as repo
import library.findbook.services as services
from library.authentication.authentication import login_required
from library.authentication.services import get_user_reviews

findbook_blueprint = Blueprint(
    'findbook_bp', __name__
)


@findbook_blueprint.route('/list', methods=['GET'])
def list_books():
    return redirect(url_for('findbook_bp.view_books'))


@findbook_blueprint.route('/find_book', methods=['GET'])
def find_book():
    book_form = BookForm()
    return render_template('findbook/findbook.html', book_form=book_form, handler_url=url_for('findbook_bp.view_books'))


@findbook_blueprint.route('/view_books', methods=['GET', 'POST'])
def view_books():
    page, per_page, offset = get_page_args()
    book_form = BookForm()
    form = ReviewForm()

    if request.method == 'POST':
        if book_form.validate_on_submit():
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
            pagination = Pagination(page=page, total=len(books))
            return render_template('findbook/displaybooks.html', books=books, pagination=pagination,
                                   book_form=book_form, form=form, handler_url=url_for('findbook_bp.add_review'))

    if request.method == 'GET':
        pagination = Pagination(page=page, total=len(repo.repo_instance))
        return render_template('findbook/displaybooks.html', books=repo.repo_instance, pagination=pagination,
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
    services.add_review(book_id, int(request.values.get("review_rating")), request.values.get("review"), user_name,
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


@findbook_blueprint.route('/view_recommendations', methods=['GET'])
@login_required
def get_recommendations():
    user_name = session['user_name']
    reviews = get_user_reviews(user_name, repo.repo_instance)
    recommendation_tuple = namedtuple("Review", ["review_rating", "book_id", "similar_books"])
    recommendation_list = []

    for review in reviews:
        book = services.get_book_by_id(review.book.book_id, repo.repo_instance)
        recommendation = recommendation_tuple(book_id=book[0].book_id, review_rating=review.rating,
                                              similar_books=book[0].similar_books)
        recommendation_list.append(recommendation)

    recommendation_list.sort()

    return render_template('findbook/bookrecommendations.html', recommendations=recommendation_list)


def Sort_Tuple(tup):
    tup.sort(key=lambda x: x[1])
    return tup


# Driver Code
tup = [('rishav', 10), ('akash', 5), ('ram', 20), ('gaurav', 15)]

# printing the sorted list of tuples
print(Sort_Tuple(tup))


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
    review_rating = IntegerField("Review Rating", [DataRequired()])
    book_id = IntegerField("Book ID")
    submit = SubmitField('Submit Review')
