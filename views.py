from flask import Blueprint, render_template
from database import GPU

views = Blueprint('views', __name__)


@views.route("/")
def home():
    return render_template("index.html")


@views.route("/learn")
def learn():
    return render_template("learn.html")


@views.route("/components")
def gpus():
    gpus = GPU.query.all()
    return render_template("components.html", gpus=gpus)
