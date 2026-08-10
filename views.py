from flask import Blueprint, render_template, request
from sqlalchemy import or_
from database import (
    GPU,
    CPU,
    Brand,
    Cooler,
    Storage,
    motherboard,
    RAM,
    PSU,
    Case,
    Fan,
)

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
        rams=RAM.query.all(),
        storage=Storage.query.all(),
        psus=PSU.query.all(),
        coolers=Cooler.query.all(),
        cases=Case.query.all(),
        case_fans=Fan.query.all()
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


@views.route("/gpu")
def gpu_list():
    q = request.args.get("q", "").strip()

    if q:
        gpus = (
            GPU.query
            .join(Brand)
            .filter(
                or_(
                    GPU.model.ilike(f"%{q}%"),
                    Brand.name.ilike(f"%{q}%")
                )
            )
            .all()
        )
    else:
        gpus = GPU.query.all()

    return render_template("gpu_list.html", gpus=gpus, q=q)


@views.route("/cpu")
def cpu_list():
    q = request.args.get("q", "").strip()

    if q:
        cpus = (
            CPU.query
            .join(Brand)
            .filter(
                or_(
                    CPU.model.ilike(f"%{q}%"),
                    Brand.name.ilike(f"%{q}%")
                )
            )
            .all()
        )
    else:
        cpus = CPU.query.all()

    return render_template("cpu_list.html", cpus=cpus, q=q)


@views.route("/motherboard")
def motherboard_list():
    q = request.args.get("q", "").strip()

    if q:
        motherboarda = (
            motherboard.query
            .join(Brand)
            .filter(
                or_(
                    motherboard.model.ilike(f"%{q}%"),
                    Brand.name.ilike(f"%{q}%")
                )
            )
            .all()
        )
    else:
        motherboarda = motherboard.query.all()

    return render_template(
        "motherboard_list.html", motherboard=motherboarda, q=q)


@views.route("/ram")
def ram_list():
    q = request.args.get("q", "").strip()

    if q:
        rams = (
            RAM.query
            .join(Brand)
            .filter(
                or_(
                    RAM.model.ilike(f"%{q}%"),
                    Brand.name.ilike(f"%{q}%")
                )
            )
            .all()
        )
    else:
        rams = RAM.query.all()

    return render_template("ram_list.html", rams=rams, q=q)


@views.route("/storage")
def storage_list():
    q = request.args.get("q", "").strip()

    if q:
        storage = (
            Storage.query
            .join(Brand)
            .filter(
                or_(
                    Storage.model.ilike(f"%{q}%"),
                    Brand.name.ilike(f"%{q}%")
                )
            )
            .all()
        )
    else:
        storage = Storage.query.all()

    return render_template("storage_list.html", storage=storage, q=q)


@views.route("/psu")
def psu_list():
    q = request.args.get("q", "").strip()

    if q:
        psus = (
            PSU.query
            .join(Brand)
            .filter(
                or_(
                    PSU.model.ilike(f"%{q}%"),
                    Brand.name.ilike(f"%{q}%")
                )
            )
            .all()
        )
    else:
        psus = PSU.query.all()

    return render_template("psu_list.html", psus=psus, q=q)


@views.route("/cooler")
def cooler_list():
    q = request.args.get("q", "").strip()

    if q:
        coolers = (
            Cooler.query
            .join(Brand)
            .filter(
                or_(
                    Cooler.model.ilike(f"%{q}%"),
                    Brand.name.ilike(f"%{q}%")
                )
            )
            .all()
        )
    else:
        coolers = Cooler.query.all()

    return render_template("cooler_list.html", coolers=coolers, q=q)


@views.route("/case")
def case_list():
    q = request.args.get("q", "").strip()

    if q:
        cases = (
            Case.query
            .join(Brand)
            .filter(
                or_(
                    Case.model.ilike(f"%{q}%"),
                    Brand.name.ilike(f"%{q}%")
                )
            )
            .all()
        )
    else:
        cases = Case.query.all()

    return render_template("case_list.html", cases=cases, q=q)


@views.route("/case_fans")
def fan_list():
    q = request.args.get("q", "").strip()

    if q:
        fans = (
            Fan.query
            .join(Brand)
            .filter(
                or_(
                    Fan.model.ilike(f"%{q}%"),
                    Brand.name.ilike(f"%{q}%")
                )
            )
            .all()
        )
    else:
        fans = Fan.query.all()

    return render_template("fan_list.html", fans=fans, q=q)
