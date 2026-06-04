import os
import shutil
from config import DEST_CLEAN_IMAGES, DEST_CLEAN_LABELS
from utils.analysis_utils import get_dataset_files, analyze_labels


def analyze_dataset():
    # Analyze the dataset for size, class distribution, and data quality issues.
    print("Dataset Analysis")
    print("=" * 60)

    image_files, label_files, image_bases, label_bases = get_dataset_files(
        DEST_CLEAN_IMAGES, DEST_CLEAN_LABELS
    )

    # Dataset size
    print("\nDataset Size")
    print(f"Images: {len(image_files)}")
    print(f"Labels: {len(label_files)}")

    # Mapping verification
    print("\nMapping Verification")
    missing_labels = image_bases - label_bases
    missing_images = label_bases - image_bases
    print(f"Missing labels: {len(missing_labels)}")
    print(f"Missing images: {len(missing_images)}")

    # Label analysis
    analysis = analyze_labels(DEST_CLEAN_LABELS)
    print("\nClass Distribution")
    for class_id, count in sorted(analysis["class_counts"].items()):
        print(f"Class {class_id}: {count} annotations")

    print(f"\nTotal annotations: {analysis['total_annotations']}")
    avg_objects = (
        analysis["total_annotations"] / len(image_files) if image_files else 0
    )
    print(f"Average objects per image: {avg_objects:.2f}")

    # Data quality
    print("\nData Quality")
    print(f"Empty labels: {len(analysis['empty_labels'])}")
    print(f"Corrupted labels: {len(analysis['corrupted_labels'])}")
    print(f"Invalid boxes: {len(analysis['invalid_boxes'])}")

    # Readiness check
    ready = not (
        missing_labels
        or missing_images
        or analysis["corrupted_labels"]
        or analysis["invalid_boxes"]
    )

    print("\nStatus")
    print("Dataset is ready for training" if ready else "Dataset needs fixing")

    organize_problematic_labels(analysis)
    verify_integrity()


def organize_problematic_labels(analysis, output_dir="issues_report"):
    # Create folders for Empty, Corrupted, and Invalid labels and copy files into them.
    os.makedirs(output_dir, exist_ok=True)

    categories = {
        "Empty labels": analysis["empty_labels"],
        "Corrupted labels": [f for f, _ in analysis["corrupted_labels"]],
        "Invalid boxes": [f for f, _ in analysis["invalid_boxes"]],
    }

    copied_any = False
    for category, files in categories.items():
        if not files:
            continue

        category_path = os.path.join(output_dir, category)
        os.makedirs(category_path, exist_ok=True)

        for file in set(files):  # avoid duplicates
            src = os.path.join(DEST_CLEAN_LABELS, file)
            dst = os.path.join(category_path, file)
            try:
                shutil.copy(src, dst)
                print(f"Copied {file} → {category}")
                copied_any = True
            except Exception as e:
                print(f"Could not copy {file}: {e}")

    if copied_any:
        print(f"\nOrganization complete! Check the '{output_dir}' folder.")
    else:
        print("\nNo problematic label files were found to organize.")


def verify_integrity(output_dir="issues_report"):
    # Compare identified problematic files with the original dataset to ensure no mismatches after organization.
    label_files = [f for f in os.listdir(DEST_CLEAN_LABELS) if f.endswith(".txt")]

    copied_files = []
    for category in ["Empty labels", "Corrupted labels", "Invalid boxes"]:
        category_path = os.path.join(output_dir, category)
        if os.path.exists(category_path):
            copied_files.extend(os.listdir(category_path))

    original_set = set(label_files)
    copied_set = set(copied_files)

    missing_in_copy = original_set.intersection(copied_set) ^ copied_set
    extra_in_copy = copied_set - original_set

    print("\nIntegrity Check")
    if not missing_in_copy and not extra_in_copy:
        print("All identified files match the original dataset.")
    else:
        if missing_in_copy:
            print(f"Missing in copy: {missing_in_copy}")
        if extra_in_copy:
            print(f"Extra in copy: {extra_in_copy}")


if __name__ == "__main__":
    analyze_dataset()
