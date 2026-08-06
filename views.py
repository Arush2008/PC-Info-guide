from flask import Blueprint, render_template
from database import (
    GPU,
    CPU,
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
    gpus = GPU.query.all()
    return render_template("gpu_list.html", gpus=gpus)


@views.route("/cpu")
def cpu_list():
    cpus = CPU.query.all()
    return render_template("cpu_list.html", cpus=cpus)


@views.route("/motherboard")
def motherboard_list():
    motherboards = motherboard.query.all()
    return render_template("motherboard_list.html", motherboards=motherboards)


@views.route("/ram")
def ram_list():
    rams = RAM.query.all()
    return render_template("ram_list.html", rams=rams)


@views.route("/storage")
def storage():
    storage_items = Storage.query.all()
    return render_template("storage_list.html", storage=storage_items)


@views.route("/psu")
def psu_list():
    psus = PSU.query.all()
    return render_template("psu_list.html", psus=psus)


@views.route("/cooler")
def cooler_list():
    coolers = Cooler.query.all()
    return render_template("cooler_list.html", coolers=coolers)


@views.route("/case")
def case_list():
    cases = Case.query.all()
    return render_template("case_list.html", cases=cases)


@views.route("/case_fans")
def case_fans_list():
    case_fans = Fan.query.all()
    return render_template("case_fans_list.html", case_fans=case_fans)
