from flask import Blueprint, render_template, request
from sqlalchemy import or_
import re
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


def _extract_number(query):
    match = re.search(r"(\d+)", query.lower())
    return int(match.group(1)) if match else None


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


@views.route("/component_list")
def component_list():
    q = request.args.get("q", "").strip()
    q_number = _extract_number(q)

    gpu_query = GPU.query.join(Brand)
    cpu_query = CPU.query.join(Brand)
    motherboard_query = motherboard.query.join(Brand)
    ram_query = RAM.query.join(Brand)
    storage_query = Storage.query.join(Brand)
    psu_query = PSU.query.join(Brand)
    cooler_query = Cooler.query.join(Brand)
    case_query = Case.query.join(Brand)
    fan_query = Fan.query.join(Brand)

    if q:
        ram_filters = [
            RAM.model.ilike(f"%{q}%"),
            Brand.name.ilike(f"%{q}%"),
            RAM.ram_type.ilike(f"%{q}%"),
        ]

        if q_number is not None:
            ram_filters.append(RAM.capacity.ilike(f"{q_number}GB%"))

        ram_query = ram_query.filter(or_(*ram_filters))

        gpu_filters = [GPU.model.ilike(f"%{q}%"), Brand.name.ilike(f"%{q}%")]
        if q_number is not None:
            gpu_filters.append(GPU.vram == q_number)
        gpu_query = gpu_query.filter(or_(*gpu_filters))

        cpu_filters = [CPU.model.ilike(f"%{q}%"), Brand.name.ilike(f"%{q}%")]
        if q_number is not None:
            cpu_filters.append(CPU.cores == q_number)
        cpu_query = cpu_query.filter(or_(*cpu_filters))

        motherboard_filters = [
            motherboard.model.ilike(f"%{q}%"),
            Brand.name.ilike(f"%{q}%"),
        ]
        if q_number is not None:
            motherboard_filters.append(motherboard.ram_slots == q_number)
        motherboard_query = motherboard_query.filter(or_(*motherboard_filters))

        storage_filters = [
            Storage.model.ilike(f"%{q}%"),
            Brand.name.ilike(f"%{q}%"),
        ]
        if q_number is not None:
            storage_filters.append(Storage.capacity == q_number)
        storage_query = storage_query.filter(or_(*storage_filters))

        psu_filters = [PSU.model.ilike(f"%{q}%"), Brand.name.ilike(f"%{q}%")]
        if q_number is not None:
            psu_filters.append(PSU.wattage == q_number)
        psu_query = psu_query.filter(or_(*psu_filters))

        cooler_query = cooler_query.filter(
            or_(Cooler.model.ilike(f"%{q}%"), Brand.name.ilike(f"%{q}%"))
        )

        case_query = case_query.filter(
            or_(Case.model.ilike(f"%{q}%"), Brand.name.ilike(f"%{q}%"))
        )

        fan_query = fan_query.filter(
            or_(Fan.model.ilike(f"%{q}%"), Brand.name.ilike(f"%{q}%"))
        )

    return render_template(
        "components_list.html",
        q=q,
        gpus=gpu_query.all(),
        cpus=cpu_query.all(),
        motherboards=motherboard_query.all(),
        rams=ram_query.all(),
        storage=storage_query.all(),
        psus=psu_query.all(),
        coolers=cooler_query.all(),
        cases=case_query.all(),
        case_fans=fan_query.all()
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
    q_number = _extract_number(q)

    if q:
        gpu_filters = [GPU.model.ilike(f"%{q}%"), Brand.name.ilike(f"%{q}%")]
        if q_number is not None:
            gpu_filters.append(GPU.vram == q_number)

        gpus = (
            GPU.query
            .join(Brand)
            .filter(or_(*gpu_filters))
            .all()
        )
    else:
        gpus = GPU.query.all()

    return render_template("gpu_list.html", gpus=gpus, q=q)


@views.route("/cpu")
def cpu_list():
    q = request.args.get("q", "").strip()
    q_number = _extract_number(q)

    if q:
        cpu_filters = [CPU.model.ilike(f"%{q}%"), Brand.name.ilike(f"%{q}%")]
        if q_number is not None:
            cpu_filters.append(CPU.cores == q_number)

        cpus = (
            CPU.query
            .join(Brand)
            .filter(or_(*cpu_filters))
            .all()
        )
    else:
        cpus = CPU.query.all()

    return render_template("cpu_list.html", cpus=cpus, q=q)


@views.route("/motherboard")
def motherboard_list():
    q = request.args.get("q", "").strip()
    q_number = _extract_number(q)

    if q:
        motherboard_filters = [
            motherboard.model.ilike(f"%{q}%"),
            Brand.name.ilike(f"%{q}%"),
        ]
        if q_number is not None:
            motherboard_filters.append(motherboard.ram_slots == q_number)

        motherboarda = (
            motherboard.query
            .join(Brand)
            .filter(or_(*motherboard_filters))
            .all()
        )
    else:
        motherboarda = motherboard.query.all()

    return render_template(
        "motherboard_list.html", motherboard=motherboarda, q=q)


@views.route("/ram")
def ram_list():
    q = request.args.get("q", "").strip()
    q_number = _extract_number(q)

    if q:
        ram_filters = [
            RAM.model.ilike(f"%{q}%"),
            Brand.name.ilike(f"%{q}%"),
            RAM.ram_type.ilike(f"%{q}%"),
        ]

        if q_number is not None:
            ram_filters.append(RAM.capacity.ilike(f"{q_number}GB%"))

        rams = (
            RAM.query
            .join(Brand)
            .filter(or_(*ram_filters))
            .all()
        )
    else:
        rams = RAM.query.all()

    return render_template("ram_list.html", rams=rams, q=q)


@views.route("/storage")
def storage_list():
    q = request.args.get("q", "").strip()
    q_number = _extract_number(q)

    if q:
        storage_filters = [
            Storage.model.ilike(f"%{q}%"),
            Brand.name.ilike(f"%{q}%"),
        ]
        if q_number is not None:
            storage_filters.append(Storage.capacity == q_number)

        storage = (
            Storage.query
            .join(Brand)
            .filter(or_(*storage_filters))
            .all()
        )
    else:
        storage = Storage.query.all()

    return render_template("storage_list.html", storage=storage, q=q)


@views.route("/psu")
def psu_list():
    q = request.args.get("q", "").strip()
    q_number = _extract_number(q)

    if q:
        psu_filters = [PSU.model.ilike(f"%{q}%"), Brand.name.ilike(f"%{q}%")]
        if q_number is not None:
            psu_filters.append(PSU.wattage == q_number)

        psus = (
            PSU.query
            .join(Brand)
            .filter(or_(*psu_filters))
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
