
from flask import Flask, render_template, flash, Blueprint,  Markup, escape, url_for, redirect
from flask_login import login_required
from .config import Config
from .forms import SearchForm


main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


@main_bp.route('/', methods=["GET", "POST"])
@login_required
def index():
    form = SearchForm()

    if form.validate_on_submit():
        search_term = form.search.data
        flash("Search term is = {}".format(search_term))

    what = {}
    what["form"] = form
    what["block"] = "<div class=\"w3-container w3-margin-top\"><p>Hello world</p></div>"
    return render_template("index.html", **what)
