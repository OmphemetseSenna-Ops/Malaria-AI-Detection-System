import os
from pathlib import Path

from config import DEST_CLEAN_IMAGES, DEST_CLEAN_LABELS, SRC_BASE

THIN_SOURCE_IMAGES = os.path.join(SRC_BASE, "Thin_Images", "images")
THIN_SOURCE_LABELS = os.path.join(SRC_BASE, "Thin_Images", "labels_yolo")


def find_empty_label_files(label_dir):
    directory = Path(label_dir)
    if not directory.is_dir():
        return []

    empty_files = []
    for label_path in directory.glob("*.txt"):
        try:
            if label_path.stat().st_size == 0 or not label_path.read_text().strip():
                empty_files.append(label_path.name)
        except Exception:
            empty_files.append(label_path.name)

    return empty_files


def remove_empty_labels(label_dir, image_dir=None, delete_images=False):
    empty_files = find_empty_label_files(label_dir)
    removed = {
        "labels": [],
        "images": []
    }

    for file_name in empty_files:
        label_path = Path(label_dir) / file_name
        if label_path.exists():
            label_path.unlink()
            removed["labels"].append(str(label_path))

        if delete_images and image_dir is not None:
            image_path = Path(image_dir) / f"{Path(file_name).stem}.jpg"
            if image_path.exists():
                image_path.unlink()
                removed["images"].append(str(image_path))

    return removed


def clean_thick_dataset(remove_images=True):
    print("Cleaning Thick dataset")
    print("=" * 24)
    removed = remove_empty_labels(
        DEST_CLEAN_LABELS,
        image_dir=DEST_CLEAN_IMAGES,
        delete_images=remove_images,
    )

    print(f"Removed {len(removed['labels'])} empty label files from Thick dataset.")
    if remove_images:
        print(f"Removed {len(removed['images'])} corresponding image files.")

    return removed


def clean_thin_dataset(remove_images=False):
    print("Cleaning Thin dataset")
    print("=" * 23)
    removed = remove_empty_labels(
        THIN_SOURCE_LABELS,
        image_dir=THIN_SOURCE_IMAGES,
        delete_images=remove_images,
    )

    print(f"Removed {len(removed['labels'])} empty label files from Thin dataset.")
    if remove_images:
        print(f"Removed {len(removed['images'])} corresponding image files.")

    return removed


def clean_datasets(remove_thick_images=True, remove_thin_images=False):
    thick_removed = clean_thick_dataset(remove_images=remove_thick_images)
    thin_removed = clean_thin_dataset(remove_images=remove_thin_images)
    return {
        "thick": thick_removed,
        "thin": thin_removed,
    }


def run():
    clean_datasets()


if __name__ == "__main__":
    run()
