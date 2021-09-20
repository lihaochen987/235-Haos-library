from flask import Blueprint, render_template, url_for

import library.utilities.utilities as utilities
import library.authentication.authentication as authentication


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/')
def home():
    return render_template(
        'home/home.html',
        register_url = url_for('authentication_bp.register'),
        login_url = url_for('authentication_bp.login'),
        find_book_url=url_for('findbook_bp.find_book'),
    )