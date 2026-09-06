from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Brand(db.Model):
    __tablename__ = 'brand'

    brand_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class GPU(db.Model):
    __tablename__ = 'gpu'

    gpu_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    brand_id = db.Column(
        db.String(50),
        db.ForeignKey('brand.brand_id'),
        nullable=False
    )
    price = db.Column(db.Numeric(10, 2), nullable=False)
    vram = db.Column(db.Integer, nullable=False)
    performance_score = db.Column(db.Integer, nullable=False)
    power_usage = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    brand = db.relationship('Brand', backref='gpus', lazy=True)


class CPU(db.Model):
    __tablename__ = 'cpu'

    cpu_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False, unique=True)
    brand_id = db.Column(
        db.String(50),
        db.ForeignKey('brand.brand_id'),
        nullable=False
    )
    price = db.Column(db.Numeric(10, 2), nullable=False)
    cores = db.Column(db.Integer, nullable=False)
    threads = db.Column(db.Integer, nullable=False)
    brand = db.relationship('Brand', backref='cpus', lazy=True)
    socket = db.Column(db.String(50), nullable=False)
    performance_score = db.Column(db.Integer, nullable=False)
    power_usage = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=False)


class motherboard(db.Model):
    __tablename__ = 'motherboard'

    motherboard_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    brand_id = db.Column(
        db.String(50),
        db.ForeignKey('brand.brand_id'),
        nullable=False
    )
    price = db.Column(db.Numeric(10, 2), nullable=False)
    ram_slots = db.Column(db.Integer, nullable=False)
    socket = db.Column(db.String(50), nullable=False)
    ram_type = db.Column("ram_type", db.String(20), nullable=False)
    form_factor = db.Column(db.String(50), nullable=False)
    power_usage = db.Column(db.Integer, nullable=False)
    brand = db.relationship('Brand', backref='motherboards', lazy=True)
    image = db.Column(db.String(100), nullable=False)


class RAM(db.Model):
    __tablename__ = 'ram'

    ram_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    ram_type = db.Column("type", db.String(20), nullable=False)
    brand_id = db.Column(
        db.String(50),
        db.ForeignKey('brand.brand_id'),
        nullable=False
    )
    price = db.Column(db.Numeric(10, 2), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    performance_score = db.Column(db.Integer, nullable=False)
    power_usage = db.Column(db.Integer, nullable=False)
    brand = db.relationship('Brand', backref='rams', lazy=True)
    image = db.Column(db.String(100), nullable=False)


class Storage(db.Model):
    __tablename__ = 'storage'

    storage_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    storage_type = db.Column("type", db.String(20), nullable=False)
    brand_id = db.Column(
        db.String(50),
        db.ForeignKey('brand.brand_id'),
        nullable=False
    )
    speed = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    power_usage = db.Column(db.Integer, nullable=False)
    brand = db.relationship('Brand', backref='storages', lazy=True)
    image = db.Column(db.String(100), nullable=False)


class PSU(db.Model):
    __tablename__ = 'psu'

    psu_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    brand_id = db.Column(
        db.String(50),
        db.ForeignKey('brand.brand_id'),
        nullable=False
    )
    efficiency_rating = db.Column(db.String(20), nullable=False)
    modular = db.Column(db.TEXT, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    wattage = db.Column(db.Integer, nullable=False)
    brand = db.relationship('Brand', backref='psus', lazy=True)
    image = db.Column(db.String(100), nullable=False)


class Cooler(db.Model):
    __tablename__ = "cooler"

    cooler_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    brand_id = db.Column(
        db.String(50),
        db.ForeignKey("brand.brand_id"),
        nullable=False
    )
    price = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    cooling_capacity = db.Column(db.String(50), nullable=False)
    radiator_size = db.Column(db.String(50), nullable=False)
    socket_support = db.Column(db.String(100), nullable=False)
    power_usage = db.Column(db.Integer, nullable=False)
    brand = db.relationship("Brand", backref="coolers", lazy=True)
    image = db.Column(db.String(100), nullable=False)


class Case(db.Model):
    __tablename__ = 'case'

    case_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    brand_id = db.Column(
        db.String(50),
        db.ForeignKey('brand.brand_id'),
        nullable=False
    )
    price = db.Column(db.Numeric(10, 2), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    form_factor = db.Column(db.String(100), nullable=False)
    brand = db.relationship('Brand', backref='cases', lazy=True)
    image = db.Column(db.String(100), nullable=False)


class Fan(db.Model):
    __tablename__ = 'fan'

    fan_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    brand_id = db.Column(
        db.String(50),
        db.ForeignKey('brand.brand_id'),
        nullable=False
    )
    price = db.Column(db.Numeric(10, 2), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    airflow = db.Column(db.String(50), nullable=False)
    noise_level = db.Column(db.String(50), nullable=False)
    brand = db.relationship('Brand', backref='case_fans', lazy=True)
    power_usage = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=False)


# Table for storing saved builds
class Builds(db.Model):
    __tablename___ = 'builds'

    build_id = db.Column(db.Integer, primary_key=True)
    build_name = db.Column(db.String(100), nullable=False)
    cpu_id = db.Column(db.Integer, db.ForeignKey('cpu.cpu_id'), nullable=False)
    gpu_id = db.Column(db.Integer, db.ForeignKey('gpu.gpu_id'), nullable=False)
    motherboard_id = db.Column(
        db.Integer,
        db.ForeignKey('motherboard.motherboard_id'),
        nullable=False)
    ram_id = db.Column(db.Integer, db.ForeignKey('ram.ram_id'), nullable=False)
    storage_id = db.Column(
        db.Integer, db.ForeignKey('storage.storage_id'),
        nullable=False)
    psu_id = db.Column(db.Integer, db.ForeignKey('psu.psu_id'), nullable=False)
    cooler_id = db.Column(
        db.Integer, db.ForeignKey('cooler.cooler_id'),
        nullable=False)
    case_id = db.Column(db.Integer, db.ForeignKey('case.case_id'),
                        nullable=False)
    fan_id = db.Column(db.Integer, db.ForeignKey('fan.fan_id'), nullable=False)

# Relationships to tell the components name.
    cpu = db.relationship("CPU")
    gpu = db.relationship("GPU")
    motherboard = db.relationship("motherboard")
    ram = db.relationship("RAM")
    storage = db.relationship("Storage")
    psu = db.relationship("PSU")
    cooler = db.relationship("Cooler")
    case = db.relationship("Case")
    fan = db.relationship("Fan")
