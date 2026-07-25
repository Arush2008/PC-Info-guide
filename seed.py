from app import app
from database import db, Storage, PSU

with app.app_context():

    storages = [

        # ================= STORAGE =================


    ]


    psus = [

        # ================= PSU =================


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