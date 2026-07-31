from pathlib import Path
import re

from app import app, db
from database import GPU


def normalise(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


with app.app_context():
    image_folder = Path(app.static_folder) / "Images for my website" / "GPUS"

    # Matches model names to image files, even if spaces/capital letters differ.
    images = {
        normalise(file.stem): file.name
        for file in image_folder.iterdir()
        if file.is_file()
    }

    for gpu in GPU.query.all():
        filename = images.get(normalise(gpu.model))

        if filename:
            gpu.image = f"Images for my website/GPUS/{filename}"
            print(f"{gpu.model} → {filename}")
        else:
            print(f"No image found for: {gpu.model}")

    db.session.commit()

print("GPU image paths updated.")