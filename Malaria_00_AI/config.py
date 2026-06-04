import os
from dotenv import load_dotenv

load_dotenv()

# Get the base directory (Malaria_00_AI folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Source paths
SRC_BASE = os.getenv(
    "SRC_BASE"
)

THICK_SOURCES = [
    os.getenv("THICK_SOURCE_1"),
    os.getenv("THICK_SOURCE_2"),
    os.getenv("THICK_SOURCE_3")
]

# Destination paths (resolved to absolute paths)
DEST_FINAL_IMAGES = os.path.join(BASE_DIR, os.getenv("DEST_FINAL_IMAGES"))
DEST_FINAL_LABELS = os.path.join(BASE_DIR, os.getenv("DEST_FINAL_LABELS"))
DEST_CLEAN_IMAGES = os.path.join(BASE_DIR, os.getenv("DEST_CLEAN_IMAGES"))
DEST_CLEAN_LABELS = os.path.join(BASE_DIR, os.getenv("DEST_CLEAN_LABELS"))

# Settings
IMAGE_EXTENSIONS = (".jpg", ".jpeg",".png")
PRIORITY_ORDER = ["Thick_P3", "Thick_P2", "Thick_P1"
]

THIN_CLASSES = [
    "gametocyte",
    "trophozoite",
    "other stage",
    "white blood cell",
    "artefacts",
    "ring stage"
]