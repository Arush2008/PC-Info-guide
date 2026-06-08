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
        GPU(model="RTX 3090", brand_id="1", vram=24, price=999.99,
            power_usage=350),
        GPU(model="RTX 3090 Ti", brand_id="1", vram=24, price=1199.99,
            power_usage=450),
        GPU(model="RTX 3080 Ti", brand_id="1", vram=12, price=999.99,
            power_usage=350),
        GPU(model="RTX 3080 12GB", brand_id="1", vram=12, price=899.99,
            power_usage=350),
        GPU(model="RTX 3080 10GB", brand_id="1", vram=10, price=849.99,
            power_usage=320),
        GPU(model="RTX 3070 Ti", brand_id="1", vram=8, price=699.99,
            power_usage=290),
        GPU(model="RTX 3070", brand_id="1", vram=8, price=599.99,
            power_usage=220),
        GPU(model="RTX 3060 Ti", brand_id="1", vram=8, price=549.99,
            power_usage=200),
        GPU(model="RTX 3060", brand_id="1", vram=12, price=499.99,
            power_usage=170),
        GPU(model="RX 6950 XT", brand_id="2", vram=16, price=999.99,
            power_usage=335),
        GPU(model="RX 6900 XT", brand_id="2", vram=16, price=899.99,
            power_usage=300),
        GPU(model="RX 6800 XT", brand_id="2", vram=16, price=799.99,
            power_usage=300),
        GPU(model="RX 6800", brand_id="2", vram=16, price=699.99,
            power_usage=250),
        GPU(model="RX 6700 XT", brand_id="2", vram=12, price=549.99,
            power_usage=230),
        GPU(model="Arc B570", brand_id="3", vram=10, price=449.99,
            power_usage=150),
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
