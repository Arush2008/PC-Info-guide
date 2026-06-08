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

    brand = db.relationship('Brand', backref='gpus', lazy=True)
