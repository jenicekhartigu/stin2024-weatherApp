from flask import Blueprint, render_template
from datetime import datetime

views = Blueprint('views',__name__)

@views.route("/")
def home():
    return render_template("index.html", now = datetime.now())