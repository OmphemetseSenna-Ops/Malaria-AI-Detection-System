import os
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")


def ensure_directory(path):
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj


def plot_class_distribution(class_counts, title="Class Distribution", class_names=None, output_path=None):
    # Plot a bar chart for class counts.

    if not class_counts:
        raise ValueError("class_counts is empty")

    labels = []
    values = []
    for cid, count in sorted(class_counts.items()):
        label = f"Class {cid}"
        if class_names is not None:
            if isinstance(class_names, dict) and cid in class_names:
                label = f"{label} ({class_names[cid]})"
            elif isinstance(class_names, (list, tuple)) and cid < len(class_names):
                label = f"{label} ({class_names[cid]})"
        labels.append(label)
        values.append(count)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=values, y=labels, palette="viridis")
    plt.title(title)
    plt.xlabel("Annotation Count")
    plt.ylabel("Class")
    plt.tight_layout()

    if output_path:
        output_path = ensure_directory(Path(output_path).parent) / Path(output_path).name
        plt.savefig(output_path, dpi=300)
        plt.close()
        return str(output_path)

    plt.show()
    return None


def plot_image_distribution(image_distribution, title="Image Distribution", output_path=None):
    # Plot a bar chart for image-level class coverage.
    if not image_distribution:
        raise ValueError("image_distribution is empty")

    labels = [key.replace("_", " ").title() for key in image_distribution.keys()]
    values = list(image_distribution.values())

    plt.figure(figsize=(10, 6))
    sns.barplot(x=values, y=labels, palette="magma")
    plt.title(title)
    plt.xlabel("Image Count")
    plt.ylabel("Category")
    plt.tight_layout()

    if output_path:
        output_path = ensure_directory(Path(output_path).parent) / Path(output_path).name
        plt.savefig(output_path, dpi=300)
        plt.close()
        return str(output_path)

    plt.show()
    return None


def save_class_distribution_figure(class_counts, output_dir="visualizations", prefix="class_distribution", class_names=None):
    output_dir = ensure_directory(output_dir)
    file_name = f"{prefix}.png"
    return plot_class_distribution(
        class_counts,
        class_names=class_names,
        output_path=output_dir / file_name,
    )


def save_image_distribution_figure(image_distribution, output_dir="visualizations", prefix="image_distribution"):
    output_dir = ensure_directory(output_dir)
    file_name = f"{prefix}.png"
    return plot_image_distribution(
        image_distribution,
        output_path=output_dir / file_name,
    )


def load_label_files(label_dir):
    if not os.path.isdir(label_dir):
        return []
    return [f for f in os.listdir(label_dir) if f.endswith(".txt")]


def compute_distribution(label_dir):
    class_counts = {}
    image_distribution = {"only_class_0": 0, "only_class_1": 0, "mixed_classes": 0, "empty_labels": 0}

    for file_name in load_label_files(label_dir):
        path = os.path.join(label_dir, file_name)
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            image_distribution["empty_labels"] += 1
            continue

        image_classes = set()
        for line in lines:
            parts = line.split()
            if len(parts) >= 1 and parts[0].isdigit():
                class_id = int(parts[0])
                class_counts[class_id] = class_counts.get(class_id, 0) + 1
                image_classes.add(class_id)

        if image_classes == {0}:
            image_distribution["only_class_0"] += 1
        elif image_classes == {1}:
            image_distribution["only_class_1"] += 1
        else:
            image_distribution["mixed_classes"] += 1

    return class_counts, image_distribution


def visualize_distributions():
    from config import DEST_CLEAN_LABELS, SRC_BASE, THIN_CLASSES

    thin_source_labels = os.path.join(SRC_BASE, "Thin_Images", "labels_yolo")

    print("Generating distribution visualizations")

    thick_counts, thick_image_dist = compute_distribution(DEST_CLEAN_LABELS)
    save_class_distribution_figure(thick_counts, prefix="thick_class_distribution")
    save_image_distribution_figure(thick_image_dist, prefix="thick_image_distribution")

    thin_counts, thin_image_dist = compute_distribution(thin_source_labels)
    save_class_distribution_figure(
        thin_counts,
        prefix="thin_class_distribution",
        class_names=THIN_CLASSES,
    )
    save_image_distribution_figure(thin_image_dist, prefix="thin_image_distribution")

    print("Visualizations saved in the visualizations directory")
