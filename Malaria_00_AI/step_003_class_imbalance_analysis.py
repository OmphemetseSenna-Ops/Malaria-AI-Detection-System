import os
from collections import defaultdict
from config import DEST_CLEAN_LABELS, SRC_BASE, THIN_CLASSES

THIN_SOURCE_LABELS = os.path.join(SRC_BASE, "Thin_Images", "labels_yolo")


def load_label_files(label_dir):
    if not os.path.isdir(label_dir):
        return []
    return [f for f in os.listdir(label_dir) if f.endswith(".txt")]


def summarize_class_distribution(label_dir, dataset_name, class_names=None):
    print(f"{dataset_name} Class Distribution")
    print("=" * (len(dataset_name) + 23))

    class_counts = defaultdict(int)
    image_distribution = {
        "only_class_0": 0,
        "only_class_1": 0,
        "mixed_classes": 0,
        "empty_labels": 0,
    }

    label_files = load_label_files(label_dir)
    if not label_files:
        print(f"No label files found for {dataset_name}. Skipping analysis.")
        return None

    for file in label_files:
        path = os.path.join(label_dir, file)
        with open(path, "r") as f:
            lines = f.readlines()

        if not lines:
            image_distribution["empty_labels"] += 1
            continue

        image_classes = set()
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            class_id = int(parts[0])
            class_counts[class_id] += 1
            image_classes.add(class_id)

        if image_classes == {0}:
            image_distribution["only_class_0"] += 1
        elif image_classes == {1}:
            image_distribution["only_class_1"] += 1
        else:
            image_distribution["mixed_classes"] += 1

    total_annotations = sum(class_counts.values())
    if total_annotations == 0:
        print("No annotations found.")
        return None

    print("\nClass Distribution")
    for cid, count in sorted(class_counts.items()):
        pct = (count / total_annotations) * 100
        label_text = f"Class {cid}" if class_names is None or cid >= len(class_names) else f"Class {cid} ({class_names[cid]})"
        print(f"{label_text}: {count:,} ({pct:.2f}%)")

    if len(class_counts) >= 2:
        majority = max(class_counts, key=class_counts.get)
        minority = min(class_counts, key=class_counts.get)
        ratio = class_counts[majority] / class_counts[minority]
        print(f"\nImbalance Ratio: Class {majority} : Class {minority} = {ratio:.2f}:1")

        if ratio < 2:
            severity = "Balanced"
        elif ratio < 5:
            severity = "Moderate imbalance"
        elif ratio < 10:
            severity = "High imbalance"
        else:
            severity = "Severe imbalance"
        print(f"Severity: {severity}")
    else:
        ratio = None

    print("\nImage Distribution")
    for key, val in image_distribution.items():
        print(f"{key.replace('_', ' ').title()}: {val}")

    print("\nTraining Recommendation")
    if ratio is not None:
        if ratio > 10:
            recs = [
                "Use class weighting",
                "Augment minority class",
                "Consider Focal Loss",
                "Monitor minority recall",
            ]
        elif ratio > 5:
            recs = ["Use moderate augmentation"]
        else:
            recs = ["Standard training is acceptable"]
        for r in recs:
            print("-", r)
    else:
        print("- Insufficient class diversity for imbalance recommendations.")

    print("\nAnalysis complete\n")
    return class_counts


def analyze_thick_class_distribution():
    summarize_class_distribution(DEST_CLEAN_LABELS, "Thick")


def analyze_thin_class_distribution():
    summarize_class_distribution(THIN_SOURCE_LABELS, "Thin", THIN_CLASSES)


def analyze_class_distribution():
    analyze_thick_class_distribution()
    analyze_thin_class_distribution()


def run():
    analyze_class_distribution()

if __name__ == "__main__":
    run()
