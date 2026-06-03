import os
from dotenv import load_dotenv

load_dotenv()

# Source paths
SRC_BASE = os.getenv(
    "SRC_BASE"
)

THICK_SOURCES = [
    os.getenv("THICK_SOURCE_1"),
    os.getenv("THICK_SOURCE_2"),
    os.getenv("THICK_SOURCE_3")
]

# Destination paths
DEST_FINAL_IMAGES = os.getenv("DEST_FINAL_IMAGES")
DEST_FINAL_LABELS = os.getenv("DEST_FINAL_LABELS")
DEST_CLEAN_IMAGES = os.getenv("DEST_CLEAN_IMAGES")
DEST_CLEAN_LABELS = os.getenv("DEST_CLEAN_LABELS")

# Settings
IMAGE_EXTENSIONS = (".jpg", ".jpeg",".png")
PRIORITY_ORDER = ["Thick_P3", "Thick_P2", "Thick_P1"
]
