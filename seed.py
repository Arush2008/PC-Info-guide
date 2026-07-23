from app import app
from database import db, CPU, Brand

with app.app_context():

    db.session.rollback()

    def get_or_create_brand(brand_id, name):
        brand = db.session.get(Brand, brand_id)

        if not brand:
            brand = Brand(
                brand_id=brand_id,
                name=name
            )
            db.session.add(brand)

        return brand


    # ----------------------------
    # CREATE BRANDS
    # ----------------------------

    get_or_create_brand(2, "AMD")
    get_or_create_brand(3, "Intel")

    db.session.commit()


    # ----------------------------
    # CPU LIST
    # ----------------------------

    cpus = [

        # ----------------------------
        # AMD CPUs
        # ----------------------------

        CPU(
            model="Ryzen 5 7600X",
            brand_id=2,
            price=435.85,
            cores=6,
            threads=12
        ),

        CPU(
            model="Ryzen 5 9600X",
            brand_id=2,
            price=458.85,
            cores=6,
            threads=12
        ),

        CPU(
            model="Ryzen 5 7500X3D",
            brand_id=2,
            price=550.85,
            cores=6,
            threads=12
        ),

        CPU(
            model="Ryzen 7 7700",
            brand_id=2,
            price=419.00,
            cores=8,
            threads=16
        ),

        CPU(
            model="Ryzen 7 7700X3D",
            brand_id=2,
            price=659.00,
            cores=8,
            threads=16
        ),

        CPU(
            model="Ryzen 7 9800X3D",
            brand_id=2,
            price=861.35,
            cores=8,
            threads=16
        ),

        CPU(
            model="Ryzen 7 9700XT",
            brand_id=2,
            price=579.00,
            cores=8,
            threads=16
        ),

        CPU(
            model="Ryzen 9 9900X",
            brand_id=2,
            price=803.85,
            cores=12,
            threads=24
        ),

        CPU(
            model="Ryzen 9 9950X",
            brand_id=2,
            price=1206.35,
            cores=16,
            threads=32
        ),

        CPU(
            model="Ryzen 9 9950X3D",
            brand_id=2,
            price=1299.01,
            cores=16,
            threads=32
        ),


        # ----------------------------
        # Intel CPUs
        # ----------------------------

        CPU(
            model="Core i7-14700F",
            brand_id=3,
            price=688.85,
            cores=20,
            threads=28
        ),

        CPU(
            model="Core Ultra 5 245KF",
            brand_id=3,
            price=401.35,
            cores=14,
            threads=14
        ),

        CPU(
            model="Core Ultra 9 285K",
            brand_id=3,
            price=1378.85,
            cores=24,
            threads=24
        ),

        CPU(
            model="Core Ultra 7 265",
            brand_id=3,
            price=550.85,
            cores=20,
            threads=20
        ),

        CPU(
            model="Core i3-12100F",
            brand_id=3,
            price=109.00,
            cores=4,
            threads=8
        ),

        CPU(
            model="Core i3-13100F",
            brand_id=3,
            price=149.00,
            cores=4,
            threads=8
        ),

        CPU(
            model="Core i5-13500",
            brand_id=3,
            price=399.00,
            cores=14,
            threads=20
        ),

        CPU(
            model="Core i7-13700K",
            brand_id=3,
            price=699.00,
            cores=16,
            threads=24
        ),

        CPU(
            model="Core i9-13900K",
            brand_id=3,
            price=899.00,
            cores=24,
            threads=32
        ),

        CPU(
            model="Core i9-13900KS",
            brand_id=3,
            price=1099.00,
            cores=24,
            threads=32
        ),

    ]


    # ----------------------------
    # INSERT SAFELY (NO DUPES)
    # ----------------------------

    for cpu in cpus:

        exists = CPU.query.filter_by(
            model=cpu.model
        ).first()

        if not exists:
            db.session.add(cpu)


    db.session.commit()

    print("CPUs added successfully!")