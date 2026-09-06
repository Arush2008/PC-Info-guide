# views.py
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for
)
import re
from pathlib import Path
from sqlalchemy.inspection import inspect
from database import (
    db,
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
    Builds
)

views = Blueprint('views', __name__)


# Function to get the first number
def _extract_number(query):
    match = re.search(r"(\d+)", query.lower())
    return int(match.group(1)) if match else None


# To define the componnets and thier IDs used for the
# builder and compatibility checks
COMPONENT_MODELS = {
    "cpu": (CPU, "cpu_id"),
    "gpu": (GPU, "gpu_id"),
    "motherboard": (motherboard, "motherboard_id"),
    "ram": (RAM, "ram_id"),
    "storage": (Storage, "storage_id"),
    "psu": (PSU, "psu_id"),
    "cooler": (Cooler, "cooler_id"),
    "case": (Case, "case_id"),
    "fan": (Fan, "fan_id"),
}

STATIC_DIRECTORY = Path(__file__).resolve().parent / "static"


# Helps to display the component name.
def get_component_display_name(item):
    brand_name = item.brand.name.strip()
    model_name = item.model.strip()
    if model_name.lower().startswith(brand_name.lower() + " "):
        return model_name
    return f"{brand_name} {model_name}"


# It helps to get the image URL for a specific component.
def get_component_image_url(item):
    image_path = getattr(item, "image", None)

    if not image_path and isinstance(item, PSU):
        candidate = f"Images for my website/PSUS/{item.model}.jpeg"
        if (STATIC_DIRECTORY / candidate).is_file():
            image_path = candidate

    return url_for("static", filename=image_path or "background.png")


# It displays the component label to show the detials of the component
def format_component_label(column_name):
    labels = {
        "vram": "VRAM",
        "ram_type": "RAM type",
        "storage_type": "Storage type",
        "psu": "PSU",
        "socket_support": "Socket support",
        "power_usage": "Power usage",
        "performance_score": "Performance score",
        "cooling_capacity": "Cooling capacity",
        "radiator_size": "Radiator size",
        "noise_level": "Noise level",
    }
    return labels.get(column_name, column_name.replace("_", " ").capitalize())


# It is used to find the specification of the component.
def get_component_specifications(model, item):
    specifications = []
    for column in inspect(model).columns:
        if column.primary_key or column.name in {"brand_id", "image", "price"}:
            continue
        attribute_name = column.name
        if column.name == "type" and model is RAM:
            attribute_name = "ram_type"
        elif column.name == "type" and model is Storage:
            attribute_name = "storage_type"

        value = getattr(item, attribute_name)
        if value is not None and value != "":
            specifications.append({
                "label": format_component_label(attribute_name),
                "value": str(value),
            })
    return specifications


# It shows the values of the filter
def get_int_filter(name):
    value = request.args.get(name, "").strip()

    try:
        return int(value) if value else None
    except ValueError:
        return None


def get_float_filter(name):
    value = request.args.get(name, "").strip()

    try:
        return float(value) if value else None
    except ValueError:
        return None


def get_filter_values():
    return {
        "brand": request.args.get("brand", "").strip(),
        "min_price": request.args.get("min_price", "").strip(),
        "max_price": request.args.get("max_price", "").strip(),
        "sort": request.args.get("sort", "name").strip(),
    }


# It displays the item based on the model and the search bar
def get_catalog_items(model, search_fields=()):
    q = request.args.get("q", "").strip()
    filters = get_filter_values()
    min_price = get_float_filter("min_price")
    max_price = get_float_filter("max_price")

    query = model.query.join(Brand)

    if q:
        search = f"%{q}%"
        query = query.filter(
            db.or_(model.model.ilike(search), Brand.name.ilike(search))
        )

    if filters["brand"]:
        query = query.filter(model.brand_id == filters["brand"])
    if min_price is not None:
        query = query.filter(model.price >= min_price)
    if max_price is not None:
        query = query.filter(model.price <= max_price)

    sort_options = {
        "name": model.model.asc(),
        "price_low": model.price.asc(),
        "price_high": model.price.desc(),
    }
    sort_order = sort_options.get(filters["sort"], model.model.asc())
    return query.order_by(sort_order).all(), q, filters


# It is used to calculate the power for the component and
# return 0 if the item is not selected or no power usage for the component.
def get_power_usage(item):
    try:
        return int(float(item.power_usage or 0))
    except (TypeError, ValueError):
        return 0


def get_numeric_value(value):
    if value is None:
        return 0
    match = re.search(r"(\d+)", str(value))
    return float(match.group(1)) if match else 0


def normalize_score(score, maximum):
    if score is None:
        return 0

    return min(round(score / maximum * 100), 100)


# It displays the score rating based on the score value.
def get_score_rating(score):
    if score is None:
        return "Not Available"
    if score >= 90:
        return "Excellent"
    if score >= 80:
        return "Very Good"
    if score >= 70:
        return "Good"
    if score >= 60:
        return "Average"

    return "Low"


# calculates the raw performance using cpu, gpu, ram and storage.
def calculate_raw_performance(cpu, gpu, ram, storage):
    if not cpu or not gpu:
        return None

    cpu_score = normalize_score(cpu.performance_score, 100)
    gpu_score = normalize_score(gpu.performance_score, 150)

    if ram:
        ram_capacity = get_numeric_value(ram.capacity)
        ram_speed = get_numeric_value(ram.speed)
        ram_capacity_score = min(ram_capacity / 32 * 100, 100)
        ram_speed_score = min(ram_speed / 6000 * 100, 100)
        ram_score = ram_capacity_score * 0.6 + ram_speed_score * 0.4
    else:
        ram_score = 40

    if storage:
        storage_speed = get_numeric_value(storage.speed)
        storage_score = min(storage_speed / 7000 * 100, 100)
    else:
        storage_score = 20

    raw_score = (
        gpu_score * 0.50
        + cpu_score * 0.30
        + ram_score * 0.10
        + storage_score * 0.10
    )

    return round(raw_score)


# It calculates the balance score using cpu, gpu and ram.
def calculate_balance_score(cpu, gpu, ram):
    if not cpu or not gpu:
        return None, "Select a CPU and GPU"

    cpu_score = normalize_score(cpu.performance_score, 100)
    gpu_score = normalize_score(gpu.performance_score, 150)

    cpu_gpu_difference = abs(cpu_score - gpu_score)
    cpu_gpu_balance = max(0, 100 - cpu_gpu_difference * 1.4)

    if not ram:
        ram_balance = 40
    else:
        ram_capacity = get_numeric_value(ram.capacity)

        if ram_capacity >= 32:
            ram_balance = 100
        elif ram_capacity >= 16:
            ram_balance = 85
        else:
            ram_balance = 55

    balance_score = round(
        cpu_gpu_balance * 0.85
        + ram_balance * 0.15
    )

    if balance_score >= 85:
        message = "Very well balanced"
    elif balance_score >= 70:
        message = "Good CPU and GPU match"
    elif balance_score >= 50:
        message = "Possible CPU or GPU bottleneck"
    else:
        message = "Major CPU and GPU imbalance"

    return balance_score, message


# calculatees the total power usage and the recommends the power value.
def get_recommended_psu(total_power, gpu_power):
    if total_power == 0:
        return 0

    headroom = 1.35 if gpu_power >= 350 else 1.25
    required_power = total_power * headroom

    standard_sizes = [450, 550, 650, 750, 850, 1000, 1200, 1600]

    for size in standard_sizes:
        if size >= required_power:
            return size

    return 1600


# to calculate the system health
def calculate_system_health(
    build,
    cpu,
    cooler,
    psu,
    recommended_wattage,
    checks,
):
    score = 100

    if not psu:
        score -= 25
    elif psu.wattage < recommended_wattage:
        score -= 35

    if cpu and not cooler:
        score -= 15
    elif cpu and cooler:
        cooling_capacity = _extract_number(cooler.cooling_capacity)

        if cooling_capacity and cooling_capacity < cpu.power_usage:
            score -= 20

    incompatible_checks = [
        check for check in checks
        if check["compatible"] is False
        and check["name"] != "PSU Wattage"
    ]

    score -= len(incompatible_checks) * 20

    required_parts = (
        "cpu",
        "gpu",
        "motherboard",
        "ram",
        "storage",
        "psu",
        "cooler",
        "case",
    )

    missing_parts = sum(
        1 for part in required_parts
        if not build.get(part)
    )

    score -= min(missing_parts * 4, 20)

    return max(score, 0)


# It show the estimated gaming performance using gpu
# and cpu and returns the resolution and fps.
def get_gaming_estimate(cpu, gpu):
    if not cpu or not gpu:
        return "Not Available", "Select a CPU and GPU"

    cpu_score = normalize_score(cpu.performance_score, 100)
    gpu_score = normalize_score(gpu.performance_score, 150)
    gaming_score = gpu_score * 0.70 + cpu_score * 0.30

    if gaming_score >= 90:
        return "4K High / Ultra", "80–140 FPS"
    if gaming_score >= 75:
        return "1440p High / Ultra", "70–120 FPS"
    if gaming_score >= 60:
        return "1440p Medium / High", "60–90 FPS"
    if gaming_score >= 48:
        return "1080p High", "60–100 FPS"
    if gaming_score >= 35:
        return "1080p Medium", "45–75 FPS"
    if gaming_score >= 22:
        return "1080p Low", "35–55 FPS"

    return "720p / 900p Low", "30–45 FPS"


# it uses all the components to calculate the performance score,
# balance score and sytem health to return the final score.
def get_build_performance():
    build = session.get("build", {})

    cpu = db.session.get(CPU, build["cpu"]) if build.get("cpu") else None
    gpu = db.session.get(GPU, build["gpu"]) if build.get("gpu") else None
    ram = db.session.get(RAM, build["ram"]) if build.get("ram") else None

    storage = (
        db.session.get(Storage, build["storage"])
        if build.get("storage") else None
    )

    cooler = (
        db.session.get(Cooler, build["cooler"])
        if build.get("cooler") else None
    )

    psu = db.session.get(PSU, build["psu"]) if build.get("psu") else None

    power_component_types = (
        "cpu",
        "gpu",
        "motherboard",
        "ram",
        "storage",
        "cooler",
        "fan",
    )

    total_power = 0

    for component_type in power_component_types:
        component_id = build.get(component_type)

        if component_id:
            model, _ = COMPONENT_MODELS[component_type]
            item = db.session.get(model, component_id)

            if item:
                total_power += get_power_usage(item)

    gpu_power = get_power_usage(gpu) if gpu else 0

    recommended_wattage = get_recommended_psu(
        total_power,
        gpu_power,
    )

    checks = check_compatibility(build)

    raw_score = calculate_raw_performance(
        cpu,
        gpu,
        ram,
        storage,
    )

    balance_score, balance_message = calculate_balance_score(
        cpu,
        gpu,
        ram,
    )

    system_health_score = calculate_system_health(
        build,
        cpu,
        cooler,
        psu,
        recommended_wattage,
        checks,
    )

    if raw_score is None or balance_score is None:
        final_score = None
    else:
        final_score = round(
            raw_score * 0.50
            + balance_score * 0.30
            + system_health_score * 0.20
        )

    gaming_resolution, gaming_fps = get_gaming_estimate(cpu, gpu)

    return {
        "performance_score": final_score,
        "performance_rating": get_score_rating(final_score),
        "raw_score": raw_score,
        "balance_score": balance_score,
        "balance_message": balance_message,
        "system_health_score": system_health_score,
        "gaming_resolution": gaming_resolution,
        "gaming_fps": gaming_fps,
        "total_power": total_power,
        "recommended_wattage": recommended_wattage,
        "psu_wattage": psu.wattage if psu else None,
        "psu_sufficient": (
            psu.wattage >= recommended_wattage
            if psu else None
        ),
    }


# Calculates the performance of the components
# and returns it as a json response.
@views.route("/api/builder/performance")
def builder_performance():
    return jsonify(get_build_performance())


def check_compatibility(build):
    results = {}

    for component_type, (model, _) in COMPONENT_MODELS.items():
        component_id = build.get(component_type)
        if component_id:
            results[component_type] = db.session.get(model, component_id)
        else:
            results[component_type] = None

    cpu = results.get("cpu")
    gpu = results.get("gpu")
    motherboard_item = results.get("motherboard")
    ram = results.get("ram")
    storage = results.get("storage")
    psu = results.get("psu")
    cooler = results.get("cooler")
    fan = results.get("fan")

    checks = []

    if cpu and motherboard_item:
        is_compatible = cpu.socket.lower() == motherboard_item.socket.lower()
        checks.append({
            "name": "CPU and Motherboard Socket Compatibility",
            "compatible": is_compatible,
            "reason": (
                f"Both use {cpu.socket}."
                if is_compatible
                else f"CPU uses {cpu.socket}, but motherboared uses "
                    f"{motherboard_item.socket}."
            )
        })
    else:
        checks.append({
            "name": "CPU and Motherboard Socket Compatibility",
            "compatible": None,
            "reason": (
                "Both CPU and Motherboard must be selected to check "
                "compatibility."
            )
        })

    if ram and motherboard_item:
        is_compatible = (
            ram.ram_type.lower() == motherboard_item.ram_type.lower()
        )

        checks.append({
            "name": "RAM and Motherboard Type",
            "compatible": is_compatible,
            "reason": (
                f"Both use {ram.ram_type}."
                if is_compatible
                else f"RAM uses {ram.ram_type}, but motherboard uses "
                    f"{motherboard_item.ram_type}."
            )
        })
    else:
        checks.append({
            "name": "RAM and Motherboard Type",
            "compatible": None,
            "reason": (
                "Both RAM and Motherboard must be selected to check "
                "compatibility."
            )
        })

    if cpu and cooler:
        is_compatible = cpu.socket.lower() in cooler.socket_support.lower()
        checks.append({
            "name": "CPU and Cooler Socket Compatibility",
            "compatible": is_compatible,
            "reason": (
                f"Cooler supports {cooler.socket_support}."
                if is_compatible
                else f"Cooler supports {cooler.socket_support}, but CPU uses "
                    f"{cpu.socket}."
            )
        })
    else:
        checks.append({
            "name": "CPU and Cooler Socket Compatibility",
            "compatible": None,
            "reason": (
                "Both CPU and Cooler must be selected to check "
                "compatibility."
            )
        })

    power_parts = [
        part for part in [
            cpu, gpu, motherboard_item, ram, storage, cooler, fan
        ]
        if part is not None
    ]

    if psu and power_parts:
        total_power = sum(
            get_power_usage(part)
            for part in power_parts
        )

        recommended_wattage = round(total_power * 1.2)

        is_compatible = psu.wattage >= recommended_wattage

        checks.append({
            "name": "PSU Wattage",
            "compatible": is_compatible,
            "reason": (
                f"Build uses about {total_power}W. "
                f"{psu.wattage}W PSU meets the "
                f"{recommended_wattage}W recommendation."
                if is_compatible
                else
                f"Build uses about {total_power}W and needs about "
                f"{recommended_wattage}W. "
                f"Your PSU is only {psu.wattage}W."
            )
        })

    else:
        checks.append({
            "name": "PSU Wattage",
            "compatible": None,
            "reason": (
                "Select a PSU and at least one power component."
            )
        })

    return checks


# Used to check the compatibility of the seleccted components
# in the builder and returns it as a json response.
@views.route("/api/builder/compatibility")
def builder_compatibility():
    build = session.get("build", {})
    return jsonify({
        "results": check_compatibility(build)
    })


def get_component_options(component_type, search_text=""):
    component_data = COMPONENT_MODELS.get(component_type)

    if component_data is None:
        return None, None

    model, id_attr = component_data
    query = model.query.join(Brand)

    components = query.order_by(model.model).all()

    if search_text:
        search_text = search_text.lower().strip()

        components = [
            item for item in components
            if (
                search_text in item.model.lower()
                or search_text in item.brand.name.lower()
            )
        ]

    return components, id_attr


# Finds the summary of the selected components.
def get_build_summary():
    build = session.get("build", {})
    selected_parts = {}
    total_price = 0

    for component_type, component_id in build.items():
        component_data = COMPONENT_MODELS.get(component_type)

        if component_data is None:
            continue

        model, _ = component_data
        item = db.session.get(model, component_id)

        if item is None:
            continue

        item_price = float(item.price)
        total_price += item_price

        selected_parts[component_type] = {
            "id": component_id,
            "name": get_component_display_name(item),
            "price": item_price,
            "image_url": get_component_image_url(item),
        }

    selected_count = len(selected_parts)
    part_total = len(COMPONENT_MODELS)

    return {
        "parts": selected_parts,
        "total_price": total_price,
        "selected_count": selected_count,
        "part_total": part_total,
        "progress_percent": round(
            selected_count / part_total * 100
        ),
    }


# Home page route
@views.route("/")
def home():
    return render_template("index.html")


# Learning page route
@views.route("/learn")
def learn():
    return render_template("learn.html")


# PC builder page route
@views.route("/PC_builder")
def PC_builder():
    return render_template("PC_builder.html")


# It takes the user to the home page from random URLS.
@views.route("/<path:patch>")
def catch_all(patch):
    return redirect(url_for("views.home"))


# finds the components opetions by searching the component type.
@views.route("/api/builder/options/<component_type>")
def builder_component_options(component_type):
    search_text = request.args.get("q", "").strip()
    items, id_attr = get_component_options(component_type, search_text)

    if items is None:
        return jsonify({"error": "Invalid component type"}), 404

    rows = []

    for item in items:
        rows.append({
            "id": getattr(item, id_attr),
            "name": get_component_display_name(item),
            "price": float(item.price),
            "image_url": get_component_image_url(item),
            "details": get_component_specifications(
                COMPONENT_MODELS[component_type][0], item
            ),
        })
    return jsonify(rows)


# to get summary of the selected components.
@views.route("/api/builder/summary")
def builder_summary():
    return jsonify(get_build_summary())


# to get the details of the components.
@views.route("/api/components/<component_type>/<int:component_id>")
def component_details(component_type, component_id):
    component_data = COMPONENT_MODELS.get(component_type)

    if component_data is None:
        return jsonify({"error": "Invalid component type"}), 404

    model, _ = component_data
    item = db.session.get(model, component_id)

    if item is None:
        return jsonify({"error": "Component not found"}), 404

    return jsonify({
        "component_type": component_type,
        "component_id": component_id,
        "brand": item.brand.name,
        "model": item.model,
        "price": float(item.price),
        "image_url": get_component_image_url(item),
        "details": get_component_specifications(model, item),
    })


# Selects the component to save it locally.
@views.route("/api/builder/selection/<component_type>", methods=["PUT"])
def select_builder_component(component_type):
    component_data = COMPONENT_MODELS.get(component_type)

    if component_data is None:
        return jsonify({"error": "Invalid component type"}), 404

    data = request.get_json(silent=True) or {}

    try:
        component_id = int(data.get("id"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid component ID"}), 400

    model, _ = component_data
    item = db.session.get(model, component_id)

    if item is None:
        return jsonify({"error": "Component not found"}), 404
    build = session.get("build", {})
    build[component_type] = component_id
    session["build"] = build
    session.modified = True
    return jsonify(get_build_summary())


# Remove button to remove the component.
@views.route("/api/builder/selection/<component_type>", methods=["DELETE"])
def remove_builder_component(component_type):
    build = session.get("build", {})
    build.pop(component_type, None)
    session["build"] = build
    session.modified = True
    return jsonify(get_build_summary())


# Clears the selected componets and return.
@views.route("/api/builder/selection", methods=["DELETE"])
def clear_builder_selection():
    session["build"] = {}
    session.modified = True
    return jsonify(get_build_summary())


# components page route
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


def normalise(text):
    raw_tokens = re.findall(r"[a-z0-9]+", str(text).lower())
    tokens = set(raw_tokens)

    for token in raw_tokens:
        match = re.fullmatch(r"(\d+)([a-z]+)", token)
        if match:
            tokens.add(match.group(1))
            tokens.add(match.group(2))

    return tokens


def matches(search_text, search_tokens):
    item_tokens = normalise(search_text)
    return all(token in item_tokens for token in search_tokens)


# Displays the component list using search and fiters.
@views.route("/component_list")
def component_list():

    q = request.args.get("q", "").strip()
    search_tokens = re.findall(r"[a-z0-9]+", q.lower())
    filters = get_filter_values()
    component_type = request.args.get("type", "").strip()
    min_price = get_float_filter("min_price")
    max_price = get_float_filter("max_price")

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
        if component_type and group["name"] != component_type:
            continue

        matched_items = [
            item for item in group["items"]
            if matches(item, group["search_text"](item))
            and (not filters["brand"] or item.brand_id == filters["brand"])
            and (min_price is None or item.price >= min_price)
            and (max_price is None or item.price <= max_price)
        ]

        if filters["sort"] == "price_low":
            matched_items.sort(key=lambda item: item.price)
        elif filters["sort"] == "price_high":
            matched_items.sort(key=lambda item: item.price, reverse=True)
        else:
            matched_items.sort(key=lambda item: item.model.lower())

        results[result_keys[group["name"]]] = matched_items

    total_results = sum(len(items) for items in results.values())

    return render_template(
        "components_list.html",
        q=q,
        filters=filters,
        component_type=component_type,
        brands=Brand.query.order_by(Brand.name).all(),
        total_results=total_results,
        **results
    )


# It is used to display the learn page for the specific component.
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


# Under are all the components only things ----------------------
@views.route("/gpu")
def gpu_list():
    gpus, q, filters = get_catalog_items(GPU)
    min_vram = get_int_filter("min_vram")
    if min_vram is not None:
        gpus = [gpu for gpu in gpus if gpu.vram >= min_vram]

    return render_template(
        "gpu_list.html",
        gpus=gpus,
        q=q,
        filters=filters,
        brands=Brand.query.order_by(Brand.name).all(),
    )


@views.route("/cpu")
def cpu_list():
    cpus, q, filters = get_catalog_items(CPU)
    return render_template(
        "cpu_list.html",
        cpus=cpus,
        q=q,
        filters=filters,
        brands=Brand.query.order_by(Brand.name).all(),
    )


@views.route("/motherboard")
def motherboard_list():
    motherboards, q, filters = get_catalog_items(motherboard)
    return render_template(
        "motherboard_list.html",
        motherboards=motherboards,
        q=q,
        filters=filters,
        brands=Brand.query.order_by(Brand.name).all(),
    )


@views.route("/ram")
def ram_list():
    rams, q, filters = get_catalog_items(RAM)
    return render_template(
        "ram_list.html",
        rams=rams,
        q=q,
        filters=filters,
        brands=Brand.query.order_by(Brand.name).all(),
    )


@views.route("/storage")
def storage_list():
    storages, q, filters = get_catalog_items(Storage)
    return render_template(
        "storage_list.html",
        storages=storages,
        q=q,
        filters=filters,
        brands=Brand.query.order_by(Brand.name).all(),
    )


@views.route("/psu")
def psu_list():
    psus, q, filters = get_catalog_items(PSU)
    return render_template(
        "psu_list.html",
        psus=psus,
        q=q,
        filters=filters,
        brands=Brand.query.order_by(Brand.name).all(),
    )


@views.route("/cooler")
def cooler_list():
    coolers, q, filters = get_catalog_items(Cooler)
    return render_template(
        "cooler_list.html",
        coolers=coolers,
        q=q,
        filters=filters,
        brands=Brand.query.order_by(Brand.name).all(),
    )


@views.route("/case")
def case_list():
    cases, q, filters = get_catalog_items(Case)
    return render_template(
        "case_list.html",
        cases=cases,
        q=q,
        filters=filters,
        brands=Brand.query.order_by(Brand.name).all(),
    )


@views.route("/case_fans")
def case_fans_list():
    fans, q, filters = get_catalog_items(Fan)
    return render_template(
        "case_fans_list.html",
        case_fans=fans,
        q=q,
        filters=filters,
        brands=Brand.query.order_by(Brand.name).all(),
    )


# Displayes the saved builds route !
@views.route("/saved_builds")
def saved_builds():
    Build = Builds.query.all()
    return render_template(
        "saved_builds.html",
        Build=Build
    )


# This route will save the build to the databse.
@views.route("/api/builder/save", methods=["POST"])
def savebuilder__build():
    build = session.get("build", {})
    required_parts = (
        "cpu",
        "gpu",
        "motherboard",
        "ram",
        "storage",
        "psu",
        "cooler",
        "case",
        "fan",
    )

    for part in required_parts:
        if part not in build:
            return jsonify({"error": f"{part} is missing"}), 400

    data = request.get_json()
    build_name = data.get("name", "")

    if not build_name:
        return jsonify({"error": "Build name is required"}), 400

    saved_build = Builds(
            build_name=build_name,
            cpu_id=build["cpu"],
            gpu_id=build["gpu"],
            motherboard_id=build["motherboard"],
            ram_id=build["ram"],
            storage_id=build["storage"],
            psu_id=build["psu"],
            cooler_id=build["cooler"],
            case_id=build["case"],
            fan_id=build["fan"],
    )

    db.session.add(saved_build)
    db.session.commit()

    return jsonify({"message": "Build saved successfully"}), 201
