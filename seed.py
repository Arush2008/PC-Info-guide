from app import app
from database import db, motherboard

with app.app_context():

    motherboards = [

    # ================= INTEL (brand_id = 3) =================

    {
        "model": "Gigabyte B860M DS3H WIFI6E",
        "brand_id": "3",
        "price": 279.00,
        "ram_slots": 4,
        "power_usage": 45
        },

        {
        "model": "ASUS TUF GAMING B860M-PLUS WIFI",
        "brand_id": "3",
        "price": 389.85,
        "ram_slots": 4,
        "power_usage": 55
        },

        {
        "model": "MSI PRO B860-P WIFI",
        "brand_id": "3",
        "price": 299.00,
        "ram_slots": 4,
        "power_usage": 50
        },

        {
        "model": "Gigabyte B760M DS3H AX",
        "brand_id": "3",
        "price": 259.00,
        "ram_slots": 4,
        "power_usage": 45
        },

        {
        "model": "MSI PRO B760M-A WIFI DDR5",
        "brand_id": "3",
        "price": 228.85,
        "ram_slots": 4,
        "power_usage": 45
        },

        {
        "model": "ASUS PRIME B760M-A WIFI",
        "brand_id": "3",
        "price": 229.00,
        "ram_slots": 4,
        "power_usage": 45
        },

        {
        "model": "Gigabyte B760 GAMING X AX",
        "brand_id": "3",
        "price": 299.00,
        "ram_slots": 4,
        "power_usage": 55
        },

        {
        "model": "MSI MAG B760 TOMAHAWK WIFI",
        "brand_id": "3",
        "price": 359.00,
        "ram_slots": 4,
        "power_usage": 60
        },

        {
        "model": "ASUS ROG STRIX B760-F GAMING WIFI",
        "brand_id": "3",
        "price": 399.00,
        "ram_slots": 4,
        "power_usage": 65
        },

        {
        "model": "Gigabyte Z790 AORUS ELITE AX",
        "brand_id": "3",
        "price": 449.00,
        "ram_slots": 4,
        "power_usage": 70
        },

        {
        "model": "MSI PRO Z790-A WIFI",
        "brand_id": "3",
        "price": 424.35,
        "ram_slots": 4,
        "power_usage": 65
        },

        {
        "model": "ASUS PRIME Z790-P WIFI",
        "brand_id": "3",
        "price": 379.00,
        "ram_slots": 4,
        "power_usage": 60
        },

        {
        "model": "MSI MAG Z790 TOMAHAWK WIFI",
        "brand_id": "3",
        "price": 479.00,
        "ram_slots": 4,
        "power_usage": 75
        },

        {
        "model": "Gigabyte Z890 AORUS ELITE WIFI7",
        "brand_id": "3",
        "price": 599.00,
        "ram_slots": 4,
        "power_usage": 75
        },

        {
        "model": "ASUS ROG STRIX Z890-F GAMING WIFI",
        "brand_id": "3",
        "price": 699.00,
        "ram_slots": 4,
        "power_usage": 80
        },


        # ================= AMD (brand_id = 2) =================

        {
        "model": "ASUS PRIME A620M-A WIFI",
        "brand_id": "2",
        "price": 189.00,
        "ram_slots": 2,
        "power_usage": 35
        },

        {
        "model": "Gigabyte A620M S2H",
        "brand_id": "2",
        "price": 159.00,
        "ram_slots": 2,
        "power_usage": 35
        },

        {
        "model": "ASRock A620M-HDV/M.2+",
        "brand_id": "2",
        "price": 169.00,
        "ram_slots": 2,
        "power_usage": 35
        },

        {
        "model": "MSI PRO B650M-A WIFI",
        "brand_id": "2",
        "price": 249.00,
        "ram_slots": 4,
        "power_usage": 45
        },

        {
        "model": "ASRock B650M PRO RS WIFI",
        "brand_id": "2",
        "price": 279.00,
        "ram_slots": 4,
        "power_usage": 50
        },

        {
        "model": "Gigabyte B650M GAMING WIFI",
        "brand_id": "2",
        "price": 239.00,
        "ram_slots": 4,
        "power_usage": 45
        },

        {
        "model": "ASUS TUF GAMING B650-PLUS WIFI",
        "brand_id": "2",
        "price": 329.00,
        "ram_slots": 4,
        "power_usage": 55
        },

        {
        "model": "Gigabyte B650 AORUS ELITE AX",
        "brand_id": "2",
        "price": 349.00,
        "ram_slots": 4,
        "power_usage": 60
        },

        {
        "model": "MSI MAG B650 TOMAHAWK WIFI",
        "brand_id": "2",
        "price": 379.00,
        "ram_slots": 4,
        "power_usage": 60
        },

        {
        "model": "ASUS ROG STRIX B650E-F GAMING WIFI",
        "brand_id": "2",
        "price": 499.00,
        "ram_slots": 4,
        "power_usage": 70
        },

        {
        "model": "ASRock B850 Steel Legend WIFI",
        "brand_id": "2",
        "price": 399.00,
        "ram_slots": 4,
        "power_usage": 60
        },

        {
        "model": "MSI MAG X670E TOMAHAWK WIFI",
        "brand_id": "2",
        "price": 499.00,
        "ram_slots": 4,
        "power_usage": 75
        },

        {
        "model": "ASRock X670E Steel Legend",
        "brand_id": "2",
        "price": 499.00,
        "ram_slots": 4,
        "power_usage": 75
        },

        {
        "model": "MSI MPG X670E CARBON WIFI",
        "brand_id": "2",
        "price": 699.00,
        "ram_slots": 4,
        "power_usage": 80
        },

        {
        "model": "ASUS ROG STRIX X870-F GAMING WIFI",
        "brand_id": "2",
        "price": 799.00,
        "ram_slots": 4,
        "power_usage": 85
        }

    ]

    for board in motherboards:
        exists = motherboard.query.filter_by(
            model=board["model"]
        ).first()

        if not exists:
            db.session.add(motherboard(**board))

    db.session.commit()

    print("Motherboards added successfully!")