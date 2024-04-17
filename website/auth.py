from flask import Blueprint

auth = Blueprint('auth',__name__)

@auth.route("/auth")
def home():
    return "AUTH"

# @auth.route("/login")
# def login():
#     return "<p>Login<p>"

# @auth.route("/logout")
# def login():
#     return "<p>Logout<p>"

# @auth.route("/sign-up")
# def login():
#     return "<p>Sing up<p>"