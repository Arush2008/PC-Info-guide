from app import app
from database import db, GPU, Brand

with app.app_context():
    db.session.rollback()

    def get_or_create_brand(brand_id, name):
        brand = db.session.get(Brand, brand_id)
        if not brand:
            brand = Brand(brand_id=brand_id, name=name)
            db.session.add(brand)
        return brand

    # Create brands
    get_or_create_brand("intel", "Intel")
    get_or_create_brand("nvidia", "NVIDIA")
    get_or_create_brand("amd", "AMD")

    db.session.commit()

    # ----------------------------
    # GPU LIST (FIXED)
    # ----------------------------

    gpus = [
    ]

    # ----------------------------
    # INSERT SAFELY (NO DUPES)
    # ----------------------------

    for gpu in gpus:
        exists = GPU.query.filter_by(model=gpu.model).first()
        if not exists:
            db.session.add(gpu)

    db.session.commit()

    print("Done")
