from app import app
from database import db, Storage, PSU

with app.app_context():

    storages = [

        # ================= SAMSUNG (brand_id = 23) =================

        {
            "model": "Samsung 990 Pro 1TB",
            "brand_id": 23,
            "storage_type": "NVMe SSD",
            "price": 510.46,
            "speed": 7450,
            "capacity": "1TB",
            "power_usage": 6
        },

        {
            "model": "Samsung 990 Pro 2TB",
            "brand_id": 23,
            "storage_type": "NVMe SSD",
            "price": 853.34,
            "speed": 7450,
            "capacity": "2TB",
            "power_usage": 6
        },

        {
            "model": "Samsung 980 Pro 1TB",
            "brand_id": 23,
            "storage_type": "NVMe SSD",
            "price": 412.12,
            "speed": 7000,
            "capacity": "1TB",
            "power_usage": 6
        },


        # ================= WESTERN DIGITAL (brand_id = 24) =================

        {
            "model": "WD Black SN850X 1TB",
            "brand_id": 24,
            "storage_type": "NVMe SSD",
            "price": 317.78,
            "speed": 7300,
            "capacity": "1TB",
            "power_usage": 6
        },

        {
            "model": "WD Black SN850X 2TB",
            "brand_id": 24,
            "storage_type": "NVMe SSD",
            "price": 761.30,
            "speed": 7300,
            "capacity": "2TB",
            "power_usage": 6
        },

        {
            "model": "WD Blue SN580 1TB",
            "brand_id": 24,
            "storage_type": "NVMe SSD",
            "price": 251.85,
            "speed": 4150,
            "capacity": "1TB",
            "power_usage": 4
        },


        # ================= KINGSTON (brand_id = 5) =================

        {
            "model": "Kingston KC3000 1TB",
            "brand_id": 5,
            "storage_type": "NVMe SSD",
            "price": 289.30,
            "speed": 7000,
            "capacity": "1TB",
            "power_usage": 6
        },

        {
            "model": "Kingston KC3000 2TB",
            "brand_id": 5,
            "storage_type": "NVMe SSD",
            "price": 464.60,
            "speed": 7000,
            "capacity": "2TB",
            "power_usage": 6
        },

        {
            "model": "Kingston NV3 1TB",
            "brand_id": 5,
            "storage_type": "NVMe SSD",
            "price": 296.24,
            "speed": 6000,
            "capacity": "1TB",
            "power_usage": 4
        },

        {
            "model": "Kingston A400 480GB",
            "brand_id": 5,
            "storage_type": "SATA SSD",
            "price": 167.76,
            "speed": 500,
            "capacity": "480GB",
            "power_usage": 2
        },


        # ================= CRUCIAL (brand_id = 8) =================

        {
            "model": "Crucial T500 1TB",
            "brand_id": 8,
            "storage_type": "NVMe SSD",
            "price": 317.78,
            "speed": 7300,
            "capacity": "1TB",
            "power_usage": 6
        },

        {
            "model": "Crucial T500 2TB",
            "brand_id": 8,
            "storage_type": "NVMe SSD",
            "price": 281.32,
            "speed": 7400,
            "capacity": "2TB",
            "power_usage": 6
        },

        {
            "model": "Crucial P3 Plus 1TB",
            "brand_id": 8,
            "storage_type": "NVMe SSD",
            "price": 317.78,
            "speed": 5000,
            "capacity": "1TB",
            "power_usage": 4
        },


        # ================= ADATA (brand_id = 9) =================

        {
            "model": "ADATA Legend 850 Lite 1TB",
            "brand_id": 9,
            "storage_type": "NVMe SSD",
            "price": 316.34,
            "speed": 5000,
            "capacity": "1TB",
            "power_usage": 5
        },

        {
            "model": "ADATA Legend 960 Max 2TB",
            "brand_id": 9,
            "storage_type": "NVMe SSD",
            "price": 623.23,
            "speed": 7400,
            "capacity": "2TB",
            "power_usage": 6
        },


        # ================= LEXAR (brand_id = 26) =================

        {
            "model": "Lexar NM790 1TB",
            "brand_id": 26,
            "storage_type": "NVMe SSD",
            "price": 320.34,
            "speed": 7400,
            "capacity": "1TB",
            "power_usage": 5
        },

        {
            "model": "Lexar NM790 2TB",
            "brand_id": 26,
            "storage_type": "NVMe SSD",
            "price": 499.99,
            "speed": 7400,
            "capacity": "2TB",
            "power_usage": 5
        },


        # ================= SOLIDIGM (brand_id = 27) =================

        {
            "model": "Solidigm P44 Pro 1TB",
            "brand_id": 27,
            "storage_type": "NVMe SSD",
            "price": 246.64,
            "speed": 7000,
            "capacity": "1TB",
            "power_usage": 5
        },


        # ================= SILICON POWER (brand_id = 28) =================

        {
            "model": "Silicon Power UD90 1TB",
            "brand_id": 28,
            "storage_type": "NVMe SSD",
            "price": 259.27,
            "speed": 5000,
            "capacity": "1TB",
            "power_usage": 4
        },

        {
            "model": "Silicon Power XS70 2TB",
            "brand_id": 28,
            "storage_type": "NVMe SSD",
            "price": 619.00,
            "speed": 7300,
            "capacity": "2TB",
            "power_usage": 6
        },


        # ================= CORSAIR (brand_id = 4) =================

        {
            "model": "Corsair MP600 Pro LPX 1TB",
            "brand_id": 4,
            "storage_type": "NVMe SSD",
            "price": 289.90,
            "speed": 7100,
            "capacity": "1TB",
            "power_usage": 6
        },

        {
            "model": "Corsair MP600 Pro LPX 2TB",
            "brand_id": 4,
            "storage_type": "NVMe SSD",
            "price": 479.86,
            "speed": 7100,
            "capacity": "2TB",
            "power_usage": 6
        },


        # ================= SEAGATE (brand_id = 25) =================

        {
            "model": "Seagate FireCuda 530 1TB",
            "brand_id": 25,
            "storage_type": "NVMe SSD",
            "price": 469.20,
            "speed": 7300,
            "capacity": "1TB",
            "power_usage": 6
        },

        {
            "model": "Seagate FireCuda 530 2TB",
            "brand_id": 25,
            "storage_type": "NVMe SSD",
            "price": 299.00,
            "speed": 7300,
            "capacity": "2TB",
            "power_usage": 6
        },

        {
            "model": "Seagate Barracuda 2TB HDD",
            "brand_id": 25,
            "storage_type": "HDD",
            "price": 295.58,
            "speed": 220,
            "capacity": "2TB",
            "power_usage": 6
        },

        {
            "model": "Seagate IronWolf 4TB HDD",
            "brand_id": 25,
            "storage_type": "HDD",
            "price": 489.35,
            "speed": 180,
            "capacity": "4TB",
            "power_usage": 8
        }


    ]



    psus = [

        # ================= CORSAIR (brand_id = 4) =================

        {
            "model": "Corsair CV550",
            "brand_id": 4,
            "price": 85.00,
            "wattage": 550,
            "efficiency_rating": "80+ Bronze",
            "modular": "Non-Modular"
        },

        {
            "model": "Corsair CX650",
            "brand_id": 4,
            "price": 109.00,
            "wattage": 650,
            "efficiency_rating": "80+ Bronze",
            "modular": "Non-Modular"
        },

        {
            "model": "Corsair RM650e",
            "brand_id": 4,
            "price": 159.00,
            "wattage": 650,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },

        {
            "model": "Corsair RM750e",
            "brand_id": 4,
            "price": 179.00,
            "wattage": 750,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },

        {
            "model": "Corsair RM850e",
            "brand_id": 4,
            "price": 219.00,
            "wattage": 850,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },


        # ================= SEASONIC (brand_id = 19) =================

        {
            "model": "Seasonic Core GM-650",
            "brand_id": 19,
            "price": 129.00,
            "wattage": 650,
            "efficiency_rating": "80+ Gold",
            "modular": "Semi-Modular"
        },

        {
            "model": "Seasonic Focus GX-750",
            "brand_id": 19,
            "price": 189.00,
            "wattage": 750,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },

        {
            "model": "Seasonic Focus GX-850",
            "brand_id": 19,
            "price": 229.00,
            "wattage": 850,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },

        {
            "model": "Seasonic Vertex GX-1000",
            "brand_id": 19,
            "price": 329.00,
            "wattage": 1000,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },


        # ================= COOLER MASTER (brand_id = 12) =================

        {
            "model": "Cooler Master MWE Bronze 650 V2",
            "brand_id": 12,
            "price": 95.00,
            "wattage": 650,
            "efficiency_rating": "80+ Bronze",
            "modular": "Non-Modular"
        },

        {
            "model": "Cooler Master MWE Gold 750 V2",
            "brand_id": 12,
            "price": 139.00,
            "wattage": 750,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },

        {
            "model": "Cooler Master MWE Gold 850 V2",
            "brand_id": 12,
            "price": 169.00,
            "wattage": 850,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },


        # ================= MSI (brand_id = 20) =================

        {
            "model": "MSI MAG A650BN",
            "brand_id": 20,
            "price": 89.00,
            "wattage": 650,
            "efficiency_rating": "80+ Bronze",
            "modular": "Non-Modular"
        },

        {
            "model": "MSI MAG A750GL PCIe 5",
            "brand_id": 20,
            "price": 159.00,
            "wattage": 750,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },

        {
            "model": "MSI MAG A850GL PCIe 5",
            "brand_id": 20,
            "price": 199.00,
            "wattage": 850,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },

        {
            "model": "ASUS TUF Gaming 650W Bronze",
            "brand_id": 21,
            "price": 119.00,
            "wattage": 650,
            "efficiency_rating": "80+ Bronze",
            "modular": "Non-Modular"
        },

        {
            "model": "ASUS TUF Gaming 750W Gold",
            "brand_id": 21,
            "price": 179.00,
            "wattage": 750,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },

        {
            "model": "ASUS TUF Gaming 850W Gold",
            "brand_id": 21,
            "price": 219.00,
            "wattage": 850,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },

        {
            "model": "ASUS ROG STRIX 1000W Gold Aura Edition",
            "brand_id": 21,
            "price": 359.00,
            "wattage": 1000,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },


        # ================= GIGABYTE (brand_id = 22) =================

        {
            "model": "Gigabyte UD750GM",
            "brand_id": 22,
            "price": 139.00,
            "wattage": 750,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },

        {
            "model": "Gigabyte UD850GM",
            "brand_id": 22,
            "price": 169.00,
            "wattage": 850,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },

        {
            "model": "Gigabyte GP-AP1000GM",
            "brand_id": 22,
            "price": 299.00,
            "wattage": 1000,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },


        # ================= BE QUIET! (brand_id = 14) =================

        {
            "model": "be quiet! System Power 10 650W",
            "brand_id": 14,
            "price": 119.00,
            "wattage": 650,
            "efficiency_rating": "80+ Bronze",
            "modular": "Non-Modular"
        },

        {
            "model": "be quiet! Pure Power 12 M 750W",
            "brand_id": 14,
            "price": 179.00,
            "wattage": 750,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },

        {
            "model": "be quiet! Pure Power 12 M 850W",
            "brand_id": 14,
            "price": 219.00,
            "wattage": 850,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },

        {
            "model": "be quiet! Dark Power 13 1000W",
            "brand_id": 14,
            "price": 399.00,
            "wattage": 1000,
            "efficiency_rating": "80+ Titanium",
            "modular": "Fully Modular"
        },


        # ================= THERMALTAKE (brand_id = 18) =================

        {
            "model": "Thermaltake Toughpower GF A3 750W",
            "brand_id": 18,
            "price": 159.00,
            "wattage": 750,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },

        {
            "model": "Thermaltake Toughpower GF A3 850W",
            "brand_id": 18,
            "price": 199.00,
            "wattage": 850,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },

        {
            "model": "Thermaltake Toughpower GF3 1000W",
            "brand_id": 18,
            "price": 329.00,
            "wattage": 1000,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },


        # ================= CORSAIR HIGH END (brand_id = 4) =================

        {
            "model": "Corsair RM1000e",
            "brand_id": 4,
            "price": 289.00,
            "wattage": 1000,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        },

        {
            "model": "Corsair RM1200x Shift",
            "brand_id": 4,
            "price": 399.00,
            "wattage": 1200,
            "efficiency_rating": "80+ Gold",
            "modular": "Fully Modular"
        }

    ]


    # ================= ADD STORAGE =================

    for storage in storages:
        exists = Storage.query.filter_by(
            model=storage["model"]
        ).first()

        if not exists:
            db.session.add(Storage(**storage))


    # ================= ADD PSU =================

    for psu in psus:
        exists = PSU.query.filter_by(
            model=psu["model"]
        ).first()

        if not exists:
            db.session.add(PSU(**psu))


    db.session.commit()

    print("Storage and PSU added successfully!")