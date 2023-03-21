import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
# from .auth import session
bp = Blueprint('landing', __name__)


@bp.route('/', methods=('GET', 'POST'))
def landing():
    return render_template('landing/landing_page.html')
