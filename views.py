from flask import Blueprint, render_template, request, redirect, url_for
from database import db, GPU, Brand

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


@views.route("/add-gpu", methods=["GET", "POST"])
def add_gpu():
    brands = Brand.query.all()

    if request.method == "POST":
        model = request.form.get("model")
        brand_id = request.form.get("brand_id")
        vram = request.form.get("vram")
        price = request.form.get("price")
        price = float(price)
        power_usage = request.form.get("power_usage")

        new_gpu = GPU(
            model=model,
            brand_id=int(brand_id),
            vram=int(vram),
            price=float(price),
            power_usage=int(power_usage)
        )

        db.session.add(new_gpu)
        db.session.commit()

        return redirect(url_for("views.gpus"))

    return render_template("add_gpu.html", brands=brands)
