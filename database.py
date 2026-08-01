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
    power_usage = db.Column(db.Integer, nullable=False)

    brand = db.relationship('Brand', backref='motherboards', lazy=True)


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
    power_usage = db.Column(db.Integer, nullable=False)

    brand = db.relationship('Brand', backref='rams', lazy=True)


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

    brand = db.relationship("Brand", backref="coolers", lazy=True)


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
    control_type = db.Column(db.String(50), nullable=False)

    brand = db.relationship('Brand', backref='case_fans', lazy=True)
