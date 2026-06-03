import os
import shutil
from collections import defaultdict
from tqdm import tqdm

from config import *

from utils.file_utils import (
    create_directory,
    get_image_files,
    get_label_files,
    get_file_size
)

from utils.verification import (
    verify_dataset
)


def analyze_source_folders():
    print("Analyzing source folders...")

    folder_stats = {}
    for src in THICK_SOURCES:
        img_dir = os.path.join(
            SRC_BASE,
            src,
            "images"
        )

        lbl_dir = os.path.join(
            SRC_BASE,
            src,
            "labels_yolo"
        )

        if not os.path.exists(img_dir):
            print(f"{src}: Missing images")
            continue

        if not os.path.exists(lbl_dir):
            print(f"{src}: Missing labels")
            continue

        images = get_image_files(
            img_dir,
            IMAGE_EXTENSIONS
        )

        labels = get_label_files(
            lbl_dir
        )

        folder_stats[src] = {
            "img_dir": img_dir,
            "lbl_dir": lbl_dir,
            "images": images,
            "labels": labels
        }

        print(
            f"{src}: "
            f"{len(images)} images, "
            f"{len(labels)} labels"
        )

    return folder_stats


def merge_dataset(folder_stats):
    copied_images = 0
    copied_labels = 0

    for src in PRIORITY_ORDER:
        if src not in folder_stats:
            continue

        stats = folder_stats[src]

        print(f"Processing {src}")
        for base_name, img_file in tqdm(
            stats["images"].items(),
            desc="Images"
        ):

            src_img = os.path.join(
                stats["img_dir"],
                img_file
            )

            dest_img = os.path.join(
                DEST_FINAL_IMAGES,
                f"{base_name}.jpg"
            )

            if os.path.exists(dest_img):
                src_size = get_file_size(src_img)
                dest_size = get_file_size(dest_img)

                if src_size == dest_size:
                    continue

                dest_img = os.path.join(
                    DEST_FINAL_IMAGES,
                    f"{src}_{base_name}.jpg"
                )

            shutil.copy2(
                src_img,
                dest_img
            )

            copied_images += 1

        for lbl_file in tqdm(
            stats["labels"],
            desc="Labels"
        ):

            base_name = os.path.splitext(
                lbl_file
            )[0]

            src_lbl = os.path.join(
                stats["lbl_dir"],
                lbl_file
            )

            dest_lbl = os.path.join(
                DEST_FINAL_LABELS,
                f"{base_name}.txt"
            )

            if os.path.exists(dest_lbl):
                src_size = get_file_size(src_lbl)
                dest_size = get_file_size(dest_lbl)

                if src_size == dest_size:
                    continue

                dest_lbl = os.path.join(
                    DEST_FINAL_LABELS,
                    f"{src}_{base_name}.txt"
                )

            shutil.copy2(
                src_lbl,
                dest_lbl
            )

            copied_labels += 1

    print("Dataset merging completed")


def create_clean_dataset():
    verification = verify_dataset(
        DEST_FINAL_IMAGES,
        DEST_FINAL_LABELS
    )

    common_bases = (
        verification["image_bases"]
        .intersection(
            verification["label_bases"]
        )
    )

    print(
        f"Perfect pairs: "
        f"{len(common_bases)}"
    )

    for base in tqdm(
        sorted(common_bases),
        desc="Cleaning dataset"
    ):

        src_img = os.path.join(
            DEST_FINAL_IMAGES,
            f"{base}.jpg"
        )

        src_lbl = os.path.join(
            DEST_FINAL_LABELS,
            f"{base}.txt"
        )

        dst_img = os.path.join(
            DEST_CLEAN_IMAGES,
            f"{base}.jpg"
        )

        dst_lbl = os.path.join(
            DEST_CLEAN_LABELS,
            f"{base}.txt"
        )

        if os.path.exists(src_img):
            shutil.copy2(
                src_img,
                dst_img
            )

        if os.path.exists(src_lbl):
            shutil.copy2(
                src_lbl,
                dst_lbl
            )


def run():
    create_directory(DEST_FINAL_IMAGES)
    create_directory(DEST_FINAL_LABELS)
    create_directory(DEST_CLEAN_IMAGES)
    create_directory(DEST_CLEAN_LABELS)

    folder_stats = (analyze_source_folders())
    merge_dataset(folder_stats)
    create_clean_dataset()


if __name__ == "__main__":
    run()