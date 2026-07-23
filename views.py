from flask import Blueprint, render_template
from database import GPU, CPU, motherboard

views = Blueprint('views', __name__)


@views.route("/")
def home():
    return render_template("index.html")


@views.route("/learn")
def learn():
    return render_template("learn.html")


@views.route("/components")
def components():
    gpus = GPU.query.all()
    cpus = CPU.query.all()
    motherboards = motherboard.query.all()

    return render_template(
        "components.html",
        gpus=gpus,
        cpus=cpus,
        motherboards=motherboards,
    )


@views.route("/learn/<component>")
def learn_component(component):

    valid_components = [
        "cpu", "gpu", "motherboard", "ram",
        "storage", "psu", "cpu_cooler",
        "case", "case_fans"
    ]

    if component not in valid_components:
        return render_template("learn.html", active="")

    return render_template("learn.html", active=component)
