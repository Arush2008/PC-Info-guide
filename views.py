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
    search_tokens = re.findall(r"[a-z0-9]+", q.lower())

    catalogue = [
        {
            "name": "gpu",
            "label": "Graphics Cards",
            "items": GPU.query.join(Brand).all(),
            "search_text": lambda item: (
                f"{item.brand.name} {item.model} gpu graphics card "
                f"{item.vram} gb vram {item.power_usage} w watt"
            ),
        },
        {
            "name": "cpu",
            "label": "Processors",
            "items": CPU.query.join(Brand).all(),
            "search_text": lambda item: (
                f"{item.brand.name} {item.model} cpu processor "
                f"{item.cores} cores {item.threads} threads"
            ),
        },
        {
            "name": "motherboard",
            "label": "Motherboards",
            "items": motherboard.query.join(Brand).all(),
            "search_text": lambda item: (
                f"{item.brand.name} {item.model} motherboard "
                f"{item.ram_slots} ram slots {item.power_usage} w watt"
            ),
        },
        {
            "name": "ram",
            "label": "Memory (RAM)",
            "items": RAM.query.join(Brand).all(),
            "search_text": lambda item: (
                f"{item.brand.name} {item.model} ram memory {item.ram_type} "
                f"{item.capacity} gb {item.speed} mhz"
            ),
        },
        {
            "name": "storage",
            "label": "Storage",
            "items": Storage.query.join(Brand).all(),
            "search_text": lambda item: (
                f"{item.brand.name} "
                f"{item.model} "
                f"storage drive "
                f"{item.storage_type} "
                f"{item.capacity} gb "
                f"{item.speed} mbps"
            ),
        },
        {
            "name": "psu",
            "label": "Power Supplies",
            "items": PSU.query.join(Brand).all(),
            "search_text": lambda item: (
                f"{item.brand.name} "
                f"{item.model} "
                f"psu power supply "
                f"{item.wattage} w "
                f"watt "
                f"{item.efficiency_rating} "
                f"{item.modular}"
            ),
        },
        {
            "name": "cooler",
            "label": "CPU Coolers",
            "items": Cooler.query.join(Brand).all(),
            "search_text": lambda item: (
                f"{item.brand.name} "
                f"{item.model} "
                f"cooler cpu cooling "
                f"{item.type} "
                f"{item.cooling_capacity} "
                f"{item.radiator_size} "
                f"{item.socket_support}"
            ),
        },
        {
            "name": "case",
            "label": "Cases",
            "items": Case.query.join(Brand).all(),
            "search_text": lambda item: (
                f"{item.brand.name} {item.model} case pc case "
                f"{item.size} {item.form_factor}"
            ),
        },
        {
            "name": "fan",
            "label": "Case Fans",
            "items": Fan.query.join(Brand).all(),
            "search_text": lambda item: (
                f"{item.brand.name} {item.model} fan case fan "
                f"{item.size} mm {item.airflow} {item.noise_level}"
            ),
        },
    ]

    def normalise(text):
        raw_tokens = re.findall(r"[a-z0-9]+", str(text).lower())
        tokens = set(raw_tokens)

        for token in raw_tokens:
            match = re.fullmatch(r"(\d+)([a-z]+)", token)
            if match:
                tokens.add(match.group(1))
                tokens.add(match.group(2))
        return tokens

    def matches(item, searchable_text):

        item_tokens = (normalise(searchable_text))
        return all(token in item_tokens for token in search_tokens)

    results = {
        "gpus": [],
        "cpus": [],
        "motherboards": [],
        "rams": [],
        "storage": [],
        "psus": [],
        "coolers": [],
        "cases": [],
        "case_fans": [],
    }

    result_keys = {
        "gpu": "gpus",
        "cpu": "cpus",
        "motherboard": "motherboards",
        "ram": "rams",
        "storage": "storage",
        "psu": "psus",
        "cooler": "coolers",
        "case": "cases",
        "fan": "case_fans",
    }

    for group in catalogue:

        matched_items = [
            item for item in group["items"]
            if matches(item, group["search_text"](item))
        ]

        results[result_keys[group["name"]]] = matched_items

    total_results = sum(len(items) for items in results.values())

    return render_template(
        "components_list.html",
        q=q,
        total_results=total_results,
        **results
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
        gpu_filters = [GPU.model.ilike(q), Brand.name.ilike(q)]
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
        cpu_filters = [CPU.model.ilike(q), Brand.name.ilike(q)]
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
            motherboard.model.ilike(q),
            Brand.name.ilike(q),
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
            RAM.model.ilike(q),
            Brand.name.ilike(q),
            RAM.ram_type.ilike(q),
        ]

        if q_number is not None:
            ram_filters.append(RAM.capacity == q_number)

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
            Storage.model.ilike(q),
            Brand.name.ilike(q),
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
        psu_filters = [PSU.model.ilike(q), Brand.name.ilike(q)]
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
                    Cooler.model.ilike(q),
                    Brand.name.ilike(q)
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
                    Case.model.ilike(q),
                    Brand.name.ilike(q)
                )
            )
            .all()
        )
    else:
        cases = Case.query.all()

    return render_template("case_list.html", cases=cases, q=q)


@views.route("/case_fans")
def case_fans_list():
    q = request.args.get("q", "").strip()

    if q:
        case_fans = (
            Fan.query
            .join(Brand)
            .filter(
                or_(
                    Fan.model.ilike(q),
                    Brand.name.ilike(q)
                )
            )
            .all()
        )
    else:
        case_fans = Fan.query.all()

    return render_template("case_fans_list.html", case_fans=case_fans, q=q)
