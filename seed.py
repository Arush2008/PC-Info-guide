from app import app, db
from database import Case

cases = [
    {"case_id": 1, "model": "NZXT H5 Flow", "brand_id": 13, "price": 159, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX"},
    {"case_id": 2, "model": "NZXT H7 Flow", "brand_id": 13, "price": 229, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX"},
    {"case_id": 3, "model": "NZXT H9 Flow", "brand_id": 13, "price": 329, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX"},

    {"case_id": 4, "model": "Lian Li Lancool 216", "brand_id": 17, "price": 169, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX"},
    {"case_id": 5, "model": "Lian Li Lancool III", "brand_id": 17, "price": 269, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX,E-ATX"},
    {"case_id": 6, "model": "Lian Li O11 Dynamic EVO", "brand_id": 17, "price": 299, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX,E-ATX"},

    {"case_id": 7, "model": "Corsair 4000D Airflow", "brand_id": 4, "price": 159, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX"},
    {"case_id": 8, "model": "Corsair 5000D Airflow", "brand_id": 4, "price": 249, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX,E-ATX"},
    {"case_id": 9, "model": "Corsair 7000D Airflow", "brand_id": 4, "price": 399, "size": "Full Tower", "form_factor": "ATX,Micro ATX,Mini ITX,E-ATX"},

    {"case_id": 10, "model": "Cooler Master TD500 Mesh", "brand_id": 12, "price": 149, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX"},
    {"case_id": 11, "model": "Cooler Master HAF 500", "brand_id": 12, "price": 249, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX,E-ATX"},
    {"case_id": 12, "model": "Cooler Master NR200P", "brand_id": 12, "price": 119, "size": "Mini Tower", "form_factor": "Mini ITX,Micro ATX"},

    {"case_id": 13, "model": "Fractal Design Pop Air", "brand_id": 29, "price": 149, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX"},
    {"case_id": 14, "model": "Fractal Design Meshify 2", "brand_id": 29, "price": 279, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX,E-ATX"},
    {"case_id": 15, "model": "Fractal Design North", "brand_id": 29, "price": 229, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX"},

    {"case_id": 16, "model": "Thermaltake View 270", "brand_id": 18, "price": 129, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX"},
    {"case_id": 17, "model": "Thermaltake View 51", "brand_id": 18, "price": 299, "size": "Full Tower", "form_factor": "ATX,Micro ATX,Mini ITX,E-ATX"},

    {"case_id": 18, "model": "Phanteks Eclipse G360A", "brand_id": 30, "price": 159, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX"},
    {"case_id": 19, "model": "Phanteks NV5", "brand_id": 30, "price": 249, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX,E-ATX"},

    {"case_id": 20, "model": "ASUS TUF Gaming GT502", "brand_id": 21, "price": 269, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX"},
    {"case_id": 21, "model": "ASUS ROG Hyperion", "brand_id": 21, "price": 899, "size": "Full Tower", "form_factor": "ATX,Micro ATX,Mini ITX,E-ATX"},

    {"case_id": 22, "model": "MSI MAG PANO 100R", "brand_id": 20, "price": 179, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX"},
    {"case_id": 23, "model": "MSI MPG GUNGNIR 300R", "brand_id": 20, "price": 249, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX"},

    {"case_id": 24, "model": "be quiet! Pure Base 500DX", "brand_id": 14, "price": 179, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX"},

    {"case_id": 25, "model": "SilverStone FARA R1", "brand_id": 31, "price": 119, "size": "Mid Tower", "form_factor": "ATX,Micro ATX,Mini ITX"}
]


with app.app_context():
    for case_data in cases:
        case = Case(**case_data)
        db.session.add(case)

    db.session.commit()

print("Cases added successfully!")