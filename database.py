from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class brand(db.Model):
    brand_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class GPU(db.Model):
    gpu_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    brand_id = db.Column(db.String(50), db.ForeignKey('brand.brand_id'),
                         nullable=False)
    price = db.Column(db.Integer, nullable=False)
    vram = db.Column(db.Integer, nullable=False)
    power_usage = db.Column(db.Integer, nullable=False)


brand.gpus = db.relationship('GPU', backref='brand', lazy=True)
