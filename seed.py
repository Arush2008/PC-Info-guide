from app import app
from database import db, Storage

storage_images = {
    "Samsung 990 Pro 1TB": "Images for my website/STORAGE/Samsung 990 Pro 1TB.jpeg",
    "Samsung 990 Pro 2TB": "Images for my website/STORAGE/Samsung 990 Pro 2TB.jpeg",
    "Samsung 980 Pro 1TB": "Images for my website/STORAGE/Samsung 980 Pro 1TB.jpeg",
    "WD Black SN850X 1TB": "Images for my website/STORAGE/WD Black SN850X 1TB.jpeg",
    "WD Black SN850X 2TB": "Images for my website/STORAGE/WD Black SN850X 2TB.jpeg",
    "WD Blue SN580 1TB": "Images for my website/STORAGE/WD Blue SN580 1TB.jpeg",
    "Kingston KC3000 1TB": "Images for my website/STORAGE/Kingston KC3000 1TB.jpeg",
    "Kingston KC3000 2TB": "Images for my website/STORAGE/Kingston KC3000 2TB.jpeg",
    "Kingston NV3 1TB": "Images for my website/STORAGE/Kingston NV3 1TB.jpeg",
    "Kingston A400 480GB": "Images for my website/STORAGE/Kingston A400 480GB.jpeg",
    "Crucial T500 1TB": "Images for my website/STORAGE/Crucial T500 1TB.jpeg",
    "Crucial T500 2TB": "Images for my website/STORAGE/Crucial T500 2TB.jpeg",
    "Crucial P3 Plus 1TB": "Images for my website/STORAGE/Crucial P3 Plus 1TB.jpeg",
    "ADATA Legend 850 Lite 1TB": "Images for my website/STORAGE/ADATA Legend 850 Lite 1TB.jpeg",
    "ADATA Legend 960 Max 2TB": "Images for my website/STORAGE/ADATA Legend 960 Max 2TB.jpeg",
    "Lexar NM790 1TB": "Images for my website/STORAGE/Lexar NM790 1TB.jpeg",
    "Lexar NM790 2TB": "Images for my website/STORAGE/Lexar NM790 2TB.jpeg",
    "Solidigm P44 Pro 1TB": "Images for my website/STORAGE/Solidigm P44 Pro 1TB.jpeg",
    "Silicon Power UD90 1TB": "Images for my website/STORAGE/Silicon Power UD90 1TB.jpeg",
    "Silicon Power XS70 2TB": "Images for my website/STORAGE/Silicon Power XS70 2TB.jpeg",
    "Corsair MP600 Pro LPX 1TB": "Images for my website/STORAGE/Corsair MP600 Pro LPX 1TB.jpeg",
    "Corsair MP600 Pro LPX 2TB": "Images for my website/STORAGE/Corsair MP600 Pro LPX 2TB.jpeg",
    "Seagate FireCuda 530 1TB": "Images for my website/STORAGE/Seagate FireCuda 530 1TB.jpeg",
    "Seagate FireCuda 530 2TB": "Images for my website/STORAGE/Seagate FireCuda 530 2TB.jpeg",
    "Seagate Barracuda 2TB HDD": "Images for my website/STORAGE/Seagate Barracuda 2TB HDD.jpeg",
    "Seagate IronWolf 4TB HDD": "Images for my website/STORAGE/Seagate IronWolf 4TB HDD.jpeg",
}

with app.app_context():

    for storage_name, image_path in storage_images.items():

        item = Storage.query.filter_by(model=storage_name).first()

        if item:
            item.image = image_path
            print(f"Updated: {storage_name}")
        else:
            print(f"NOT FOUND: {storage_name}")

    db.session.commit()

print("Storage images updated successfully!")