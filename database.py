"""This file contains all the database models for the website
including the components and saved builds. It uses SQALchemy
to create the database and tables. The builds table is an idea
of many to many relationship between the buyilds. The other
tables are mainly components and brand for all the components. """

# SQLAlchemy model classes mainly define columns and relationships.
# pylint: disable=too-few-public-methods,invalid-name

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Brand(db.Model):
    """Store the brand name for all components."""
    __tablename__ = 'brand'

    brand_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class GPU(db.Model):
    """Store graphics-card specifications."""
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
    """Store CPU specifications."""
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
    """Store motherboard specifications."""
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
    """Store memory specifications."""
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
    """Store storage specifications."""
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
    """Store power-supply specifications."""
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
    """Store CPU-cooler specifications."""
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
    """Store case specifications."""
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
    """Store case-fan specifications."""
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
class Build(db.Model):
    """Store saved builds with their associated components."""
    __tablename__ = "Build"

    build_id = db.Column(db.Integer, primary_key=True)
    build_name = db.Column(db.String(100), unique=True)

    components = db.relationship(
        "BuildComponent",
        backref="build",
        cascade="all, delete-orphan"
    )


class BuildComponent(db.Model):
    """Store the association between builds and their components."""
    __tablename__ = "BuildComponent"

    build_component_id = db.Column(db.Integer, primary_key=True)
    build_id = db.Column(
        db.Integer,
        db.ForeignKey("Build.build_id"),
        nullable=False
    )
    component_type = db.Column(db.String(50), nullable=False)
    component_id = db.Column(db.Integer, nullable=False)
