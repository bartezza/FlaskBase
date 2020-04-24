
from flask import Flask, render_template, flash, Blueprint,  Markup, escape, url_for, redirect
from flask_login import login_required
from .config import Config
from .forms import SearchForm
from .layout import Layout
from .utils_html import Navigation


main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


class MyNavigation(Navigation):
    def setup(self):
        self.add_page("home", "/?", "Home")


@main_bp.route('/', methods=["GET", "POST"])
@login_required
def index():
    layout = Layout(navigation=MyNavigation("home"), title="LoLpWn")

    form = SearchForm()

    if form.validate_on_submit():
        search_term = form.search.data
        flash("Search term is = {}".format(search_term))
    
    # NOTE: do NOT store form.hidden_tag() directly in the variable since it's
    # not a normal string!
    form_html = str(form.hidden_tag())
    form_html += "<p>{search_label}: {search} {submit}</p>"\
                 .format(search_label=form.search.label, search=form.search(size=64),
                 submit=form.submit())
    layout.add_form(form_html)

    buttons = [
        {"href": "?blabla=1", "text": "Button 1"},
        {"href": "?blabla=2", "text": "Button 2"}
    ]
    layout.add_toolbar(buttons)

    return layout.finish()
    # return render_template("index.html", **what)
