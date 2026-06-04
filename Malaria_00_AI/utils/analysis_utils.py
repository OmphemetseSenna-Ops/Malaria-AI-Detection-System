import os
from collections import defaultdict
from config import IMAGE_EXTENSIONS

def get_dataset_files(image_dir, label_dir):
    #Return image files, label files, and their base names.
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(IMAGE_EXTENSIONS)]
    label_files = [f for f in os.listdir(label_dir) if f.endswith(".txt")]

    image_bases = {os.path.splitext(f)[0] for f in image_files}
    label_bases = {os.path.splitext(f)[0] for f in label_files}

    return image_files, label_files, image_bases, label_bases


def analyze_labels(label_dir):
    #Analyze YOLO label files for class counts and errors.
    class_counts = defaultdict(int)
    total_annotations = 0
    empty_labels, corrupted_labels, invalid_boxes = [], [], []

    label_files = [f for f in os.listdir(label_dir) if f.endswith(".txt")]

    for file in label_files:  # foreach-like loop
        path = os.path.join(label_dir, file)
        try:
            with open(path, "r") as f:
                lines = f.readlines()

            if not lines:
                empty_labels.append(file)
                continue

            for line_num, line in enumerate(lines, start=1):
                parts = line.strip().split()

                # YOLO format: class x y w h
                if len(parts) != 5:
                    corrupted_labels.append((file, line_num))
                    continue

                try:
                    class_id = int(parts[0])
                    x, y, w, h = map(float, parts[1:])
                except ValueError:
                    corrupted_labels.append((file, line_num))
                    continue

                class_counts[class_id] += 1
                total_annotations += 1

                if not all(0 <= val <= 1 for val in (x, y, w, h)):
                    invalid_boxes.append((file, line_num))

        except Exception:
            corrupted_labels.append((file, "read_error"))

    return {
        "class_counts": class_counts,
        "total_annotations": total_annotations,
        "empty_labels": empty_labels,
        "corrupted_labels": corrupted_labels,
        "invalid_boxes": invalid_boxes,
    }
