import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from FlaskApp.db import get_db

bp = Blueprint('error', __name__, url_prefix='/error')




# ***************************************************#
# #### ---- ERROR HANDLING ---- #####
# ***************************************************#
@bp.route('/robots.txt/')
def robots():
    return("User-agent: *\nDisallow: /register/\nDisallow: /login/\n")



# 404 - page not found error
@bp.errorhandler(404)
def page_not_found(error):
    try:
        return render_template("405.html"), 405
    except Exception as e:
        raise e


# Handle 405 method not allowed
@bp.errorhandler(405)
def method_not_found(error):
    try:
        return render_template("404.html"), 404
    except Exception as e:
        raise e


# 500 error is an unknown internal server error.
@bp.errorhandler(500)
def method_not_found(error):
    try:
        return render_template("500.html"), 500
    except Exception as e:
        raise e
