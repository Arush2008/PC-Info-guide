from app import app
from database import db, CPU

cpu_images = {
    1: "Images for my website/CPUS/Ryzen 5 7600.jpeg",
    2: "Images for my website/CPUS/Ryzen 5 5600.jpeg",
    3: "Images for my website/CPUS/Ryzen 5 5600X.jpeg",
    4: "Images for my website/CPUS/Ryzen 7 5700X.jpeg",
    5: "Images for my website/CPUS/Ryzen 7 5800X.jpeg",
    6: "Images for my website/CPUS/Ryzen 7 5800X3D.jpeg",
    7: "Images for my website/CPUS/Ryzen 7 5800XT.jpeg",
    8: "Images for my website/CPUS/Ryzen 7 7800X3D.jpeg",
    9: "Images for my website/CPUS/Ryzen 7 9700X.jpeg",
    10: "Images for my website/CPUS/Ryzen 9 7900X.jpeg",
    11: "Images for my website/CPUS/Ryzen 9 7900X3D.jpeg",
    12: "Images for my website/CPUS/Ryzen 9 7950X.jpeg",
    13: "Images for my website/CPUS/Core i5-12400F.jpeg",
    14: "Images for my website/CPUS/Core i5-13400F.jpeg",
    15: "Images for my website/CPUS/Core i5-14400F.jpeg",
    16: "Images for my website/CPUS/Core i5-14600K.jpeg",
    17: "Images for my website/CPUS/Core i7-14700.jpeg",
    18: "Images for my website/CPUS/Core i7-14700K.jpeg",
    19: "Images for my website/CPUS/Core i9-14900K.jpeg",
    20: "Images for my website/CPUS/Core Ultra 7 265K.jpeg",
    21: "Images for my website/CPUS/Ryzen 5 7600X.jpeg",
    22: "Images for my website/CPUS/Ryzen 5 9600X.jpeg",
    23: "Images for my website/CPUS/Ryzen 5 7500X3D.jpeg",
    24: "Images for my website/CPUS/Ryzen 7 7700.jpeg",
    25: "Images for my website/CPUS/Ryzen 7 7700X3D.jpeg",
    26: "Images for my website/CPUS/Ryzen 7 9800X3D.jpeg",
    27: "Images for my website/CPUS/Ryzen 7 9700XT.jpeg",
    28: "Images for my website/CPUS/Ryzen 9 9900X.jpeg",
    29: "Images for my website/CPUS/Ryzen 9 9950X.jpeg",
    30: "Images for my website/CPUS/Ryzen 9 9950X3D.jpeg",
    31: "Images for my website/CPUS/Core i7-14700F.jpeg",
    32: "Images for my website/CPUS/Core Ultra 5 245KF.jpeg",
    33: "Images for my website/CPUS/Core Ultra 9 285K.jpeg",
    34: "Images for my website/CPUS/Core Ultra 7 265.jpeg",
    35: "Images for my website/CPUS/Core i3-12100F.jpeg",
    36: "Images for my website/CPUS/Core i3-13100F.jpeg",
    37: "Images for my website/CPUS/Core i5-13500.jpeg",
    38: "Images for my website/CPUS/Core i7-13700K.jpeg",
    39: "Images for my website/CPUS/Core i9-13900K.jpeg",
    40: "Images for my website/CPUS/Core i9-13900KS.jpeg",
}

with app.app_context():
    for cpu_id, image in cpu_images.items():
        cpu = db.session.get(CPU, cpu_id)

        if cpu:
            cpu.image = image

    db.session.commit()

print("CPU images updated successfully!")