from flask import Blueprint, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired

import library.book.services as services
import library.adapters.memory_repository as repo

findbook_blueprint = Blueprint(
    'findbook_bp', __name__
)