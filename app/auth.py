
from typing import List
from flask import redirect, render_template, flash, Blueprint, request, url_for
from flask_login import login_required, logout_user, current_user, login_user, UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import (Form,
                     StringField,
                     PasswordField,
                     SubmitField)
from wtforms.validators import (DataRequired,
                                Email,
                                EqualTo,
                                Length,
                                Optional)
from flask_login import LoginManager


auth_bp = Blueprint("auth_bp", __name__,
                    template_folder="templates",
                    static_folder="static")


DEFAULT_REDIRECT = "main_bp.index"

USER_DETAILS = {
    "user": {
        "id": "user",
        "passwords": ["sha256$YX42GT9a$2477aec76a41f3caf3dc083bc30f1a0b04428829b36a94eeb74ea5d385835561"],
        "admin": True
    }
}


class SimpleUser(UserMixin):
    @property
    def passwords(self):
        return self._data["passwords"]

    def __init__(self, data):
        self._data = data

    def get_id(self):
        return self._data["id"]

    def check_password(self, password):
        for p in self._data["passwords"]:
            if check_password_hash(p, password):
                return True
        return False


# login_manager = None
login_manager = LoginManager()
app_users = []  # type: List[SimpleUser]


def init_login(the_app):
    global login_manager
    # login_manager = LoginManager()
    login_manager.init_app(the_app)

    global app_users
    users = []
    for k, u in USER_DETAILS.items():
        users.append(SimpleUser(data=u))
    app_users = {u.get_id(): u for u in users}


class LoginForm(Form):
    """User Login Form."""

    # email = StringField("Email", validators=[DataRequired("Please enter a valid email address."),
    #                                          Email("Please enter a valid email address.")])
    password = PasswordField("Password", validators=[DataRequired("Password is required")])
    submit = SubmitField("Login")


def check_password(password: str):
    global app_users
    for user_id, user in app_users.items():
        if user.check_password(password):
            return user
    return None



@auth_bp.route("/login", methods=["GET", "POST"])
def login_page():
    """User login page."""
    # Bypass Login screen if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for(DEFAULT_REDIRECT))
    login_form = LoginForm(request.form)
    # POST: Create user and redirect them to the app
    if request.method == "POST":
        if login_form.validate():
            # Get Form Fields
            # email = request.form.get("email")
            password = request.form.get("password")
            # Validate Login Attempt
            user = check_password(password=password)
            if user is not None:
                login_user(user)
                nnext = request.args.get("next")
                return redirect(nnext or url_for(DEFAULT_REDIRECT))
        flash("Invalid password")
        return redirect(url_for("auth_bp.login_page"))

    return render_template("login.html", form=LoginForm())


@login_manager.user_loader
def load_user(user_id):
    global app_users
    if user_id is not None:
        return app_users.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash("Unauthorized")
    return redirect(url_for("auth_bp.login_page"))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login_page"))


if __name__ == "__main__":
    from werkzeug.security import generate_password_hash

    password = input("Enter password to hash: ")
    hash = generate_password_hash(password, method="sha256")
    print(hash)
