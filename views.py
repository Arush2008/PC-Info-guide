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
)

views = Blueprint('views', __name__)


def _extract_number(query):
    match = re.search(r"(\d+)", query.lower())
    return int(match.group(1)) if match else None


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


def get_gaming_estimate(score):
    if score is None:
        return "Not Available", "Select a CPU and GPU"

    if score >= 90:
        return "4K High / Ultra", "80–140 FPS"
    if score >= 75:
        return "1440p High / Ultra", "70–120 FPS"
    if score >= 60:
        return "1440p Medium / High", "60–90 FPS"
    if score >= 45:
        return "1080p High", "60–100 FPS"

    return "1080p Medium", "40–70 FPS"


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

    gaming_resolution, gaming_fps = get_gaming_estimate(final_score)

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
            "name": f"{item.brand.name} {item.model}",
            "price": item_price,
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


@views.route("/")
def home():
    return render_template("index.html")


@views.route("/learn")
def learn():
    return render_template("learn.html")


@views.route("/PC_builder")
def PC_builder():
    return render_template("PC_builder.html")


@views.route("/<path:patch>")
def catch_all(patch):
    return redirect(url_for("views.home"))


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
            "name": f"{item.brand.name} {item.model}",
            "price": float(item.price),
        })
    return jsonify(rows)


@views.route("/api/builder/summary")
def builder_summary():
    return jsonify(get_build_summary())


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


@views.route("/api/builder/selection/<component_type>", methods=["DELETE"])
def remove_builder_component(component_type):
    build = session.get("build", {})
    build.pop(component_type, None)
    session["build"] = build
    session.modified = True
    return jsonify(get_build_summary())


@views.route("/api/builder/selection", methods=["DELETE"])
def clear_builder_selection():
    session["build"] = {}
    session.modified = True
    return jsonify(get_build_summary())


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
    filter = get_filter_values()

    min_price = get_float_filter("min_price")
    max_price = get_float_filter("max_price")
    min_vram = get_int_filter("min_vram")
    max_power = get_int_filter("max_power")

    query = GPU.query.join(Brand)

    if filter["brand"]:
        query = query.filter(GPU.brand_id == filter["brand"])

    if min_price is not None:
        query = query.filter(GPU.price >= min_price)

    if max_price is not None:
        query = query.filter(GPU.price <= max_price)

    if min_vram is not None:
        query = query.filter(GPU.vram >= min_vram)

    if max_power is not None:
        query = query.filter(GPU.power_usage <= max_power)

    sort_options = {
        "name": GPU.model.asc(),
        "price_low": GPU.price.asc(),
        "price_high": GPU.price.desc(),
        "vram_high": GPU.vram.desc(),
        "performance_high": GPU.performance_score.desc(),
    }

    gpus = query.order_by(
        sort_options.get(filter["sort"], GPU.model.asc())
    ).all()

    return render_template(
        "gpu_list.html",
        gpus=gpus,
        q=q,
        filters=filter,
        brands=Brand.query.order_by(Brand.name).all(),
    )


@views.route("/cpu")
def cpu_list():
    q = request.args.get("q", "").strip()
    search_tokens = re.findall(r"[a-z0-9]+", q.lower())

    cpus = CPU.query.join(Brand).all()

    def normalise(text):
        raw_tokens = re.findall(r"[a-z0-9]+", str(text).lower())
        tokens = set(raw_tokens)

        for token in raw_tokens:
            match = re.fullmatch(r"(\d+)([a-z]+)", token)
            if match:
                tokens.add(match.group(1))
                tokens.add(match.group(2))
        return tokens

    def matches(item):
        search_text = (
            f"{item.brand.name} "
            f"{item.model} "
            f"cpu processor "
            f"{item.cores} cores "
            f"{item.price}"
        )
        item_tokens = normalise(search_text)
        return all(token in item_tokens for token in search_tokens)

    cpus = [cpu for cpu in cpus if matches(cpu)]

    return render_template("cpu_list.html", cpus=cpus, q=q)


@views.route("/motherboard")
def motherboard_list():
    q = request.args.get("q", "").strip()
    search_tokens = re.findall(r"[a-z0-9]+", q.lower())

    motherboards = motherboard.query.join(Brand).all()

    def normalise(text):
        raw_tokens = re.findall(r"[a-z0-9]+", str(text).lower())
        tokens = set(raw_tokens)

        for token in raw_tokens:
            match = re.fullmatch(r"(\d+)([a-z]+)", token)
            if match:
                tokens.add(match.group(1))
                tokens.add(match.group(2))
        return tokens

    def matches(item):
        search_text = (
            f"{item.brand.name} "
            f"{item.model} "
            f"motherboard "
            f"{item.ram_slots} ram slots "
            f"{item.price}"
        )
        item_tokens = normalise(search_text)
        return all(token in item_tokens for token in search_tokens)

    motherboards = [
        motherboard for motherboard in motherboards if matches(motherboard)
        ]

    return render_template(
        "motherboard_list.html", motherboards=motherboards, q=q)


@views.route("/ram")
def ram_list():
    q = request.args.get("q", "").strip()
    search_tokens = re.findall(r"[a-z0-9]+", q.lower())

    rams = RAM.query.join(Brand).all()

    def normalise(text):
        raw_tokens = re.findall(r"[a-z0-9]+", str(text).lower())
        tokens = set(raw_tokens)

        for token in raw_tokens:
            match = re.fullmatch(r"(\d+)([a-z]+)", token)
            if match:
                tokens.add(match.group(1))
                tokens.add(match.group(2))
        return tokens

    def matches(item):
        search_text = (
            f"{item.brand.name} "
            f"{item.model} "
            f"ram "
            f"{item.capacity} gb "
            f"{item.price}"
        )
        item_tokens = normalise(search_text)
        return all(token in item_tokens for token in search_tokens)

    rams = [ram for ram in rams if matches(ram)]

    return render_template("ram_list.html", rams=rams, q=q)


@views.route("/storage")
def storage_list():
    q = request.args.get("q", "").strip()
    search_tokens = re.findall(r"[a-z0-9]+", q.lower())

    storages = Storage.query.join(Brand).all()

    def normalise(text):
        raw_tokens = re.findall(r"[a-z0-9]+", str(text).lower())
        tokens = set(raw_tokens)

        for token in raw_tokens:
            match = re.fullmatch(r"(\d+)([a-z]+)", token)
            if match:
                tokens.add(match.group(1))
                tokens.add(match.group(2))
        return tokens

    def matches(item):
        search_text = (
            f"{item.brand.name} "
            f"{item.model} "
            f"storage drive "
            f"{item.capacity} gb "
            f"{item.price}"
        )
        item_tokens = normalise(search_text)
        return all(token in item_tokens for token in search_tokens)

    storages = [storage for storage in storages if matches(storage)]

    return render_template("storage_list.html", storages=storages, q=q)


@views.route("/psu")
def psu_list():
    q = request.args.get("q", "").strip()
    search_tokens = re.findall(r"[a-z0-9]+", q.lower())

    psus = PSU.query.join(Brand).all()

    def normalise(text):
        raw_tokens = re.findall(r"[a-z0-9]+", str(text).lower())
        tokens = set(raw_tokens)

        for token in raw_tokens:
            match = re.fullmatch(r"(\d+)([a-z]+)", token)
            if match:
                tokens.add(match.group(1))
                tokens.add(match.group(2))
        return tokens

    def matches(item):
        search_text = (
            f"{item.brand.name} "
            f"{item.model} "
            f"psu power supply "
            f"{item.price}"
        )
        item_tokens = normalise(search_text)
        return all(token in item_tokens for token in search_tokens)

    psus = [psu for psu in psus if matches(psu)]

    return render_template("psu_list.html", psus=psus, q=q)


@views.route("/cooler")
def cooler_list():
    q = request.args.get("q", "").strip()
    search_tokens = re.findall(r"[a-z0-9]+", q.lower())

    coolers = Cooler.query.join(Brand).all()

    def normalise(text):
        raw_tokens = re.findall(r"[a-z0-9]+", str(text).lower())
        tokens = set(raw_tokens)

        for token in raw_tokens:
            match = re.fullmatch(r"(\d+)([a-z]+)", token)
            if match:
                tokens.add(match.group(1))
                tokens.add(match.group(2))
        return tokens

    def matches(item):
        search_text = (
            f"{item.brand.name} "
            f"{item.model} "
            f"cooler cpu cooling "
            f"{item.price}"
        )
        item_tokens = normalise(search_text)
        return all(token in item_tokens for token in search_tokens)

    coolers = [cooler for cooler in coolers if matches(cooler)]

    return render_template("cooler_list.html", coolers=coolers, q=q)


@views.route("/case")
def case_list():
    q = request.args.get("q", "").strip()
    search_tokens = re.findall(r"[a-z0-9]+", q.lower())

    cases = Case.query.join(Brand).all()

    def normalise(text):
        raw_tokens = re.findall(r"[a-z0-9]+", str(text).lower())
        tokens = set(raw_tokens)

        for token in raw_tokens:
            match = re.fullmatch(r"(\d+)([a-z]+)", token)
            if match:
                tokens.add(match.group(1))
                tokens.add(match.group(2))
        return tokens

    def matches(item):
        search_text = (
            f"{item.brand.name} "
            f"{item.model} "
            f"case pc case "
            f"{item.price}"
        )
        item_tokens = normalise(search_text)
        return all(token in item_tokens for token in search_tokens)

    cases = [case for case in cases if matches(case)]

    return render_template("case_list.html", cases=cases, q=q)


@views.route("/case_fans")
def case_fans_list():
    q = request.args.get("q", "").strip()
    search_tokens = re.findall(r"[a-z0-9]+", q.lower())

    fans = Fan.query.join(Brand).all()

    def normalise(text):
        raw_tokens = re.findall(r"[a-z0-9]+", str(text).lower())
        tokens = set(raw_tokens)

        for token in raw_tokens:
            match = re.fullmatch(r"(\d+)([a-z]+)", token)
            if match:
                tokens.add(match.group(1))
                tokens.add(match.group(2))
        return tokens

    def matches(item):
        search_text = (
            f"{item.brand.name} "
            f"{item.model} "
            f"case fan "
            f"{item.price}"
        )
        item_tokens = normalise(search_text)
        return all(token in item_tokens for token in search_tokens)

    fans = [fan for fan in fans if matches(fan)]

    return render_template("case_fans_list.html", case_fans=fans, q=q)
