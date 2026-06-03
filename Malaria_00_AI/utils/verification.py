import os

def find_gaps(bases):
    # Find missing numeric sequence.
    numeric_bases = []
    for base in bases:
        try:
            numeric_bases.append(int(base))
        except ValueError:
            continue

    if not numeric_bases:
        return []

    numeric_bases.sort()
    gaps = []

    for prev, curr in zip(numeric_bases, numeric_bases[1:]):
        if curr - prev > 1:
            gaps.append((prev, curr))

    return gaps


def verify_dataset(image_dir, label_dir):
    images = sorted([
        f for f in os.listdir(image_dir)
        if f.lower().endswith(
            (".jpg", ".jpeg", ".png")
        )
    ])

    labels = sorted([
        f for f in os.listdir(label_dir)
        if f.endswith(".txt")
    ])

    image_bases = {
        os.path.splitext(f)[0] for f in images
    }

    label_bases = {
        os.path.splitext(f)[0] for f in labels
    }

    images_without_labels = (image_bases - label_bases)
    labels_without_images = (label_bases - image_bases)

    return {
        "images": len(images),
        "labels": len(labels),
        "image_bases": image_bases,
        "label_bases": label_bases,
        "images_without_labels":
            images_without_labels,
        "labels_without_images":
            labels_without_images,
    }