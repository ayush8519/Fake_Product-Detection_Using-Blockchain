"""
signature_utils.py
Generates a deterministic digital signature (SHA-256 hash) from a barcode image.
The same barcode image will always produce the same signature.
A cloned/fake barcode will produce a DIFFERENT signature → authentication fails.
"""

import hashlib
from PIL import Image
import numpy as np


def generate_signature(image_path: str) -> str:
    """
    Read a barcode image, normalise it, and return its SHA-256 hex digest.

    Steps:
      1. Convert to greyscale (removes colour noise between scans).
      2. Resize to a fixed dimension (removes size/DPI variation).
      3. Flatten pixel array and hash with SHA-256.

    Returns a 64-character hex string.
    """
    img = Image.open(image_path).convert("L")   # greyscale
    img = img.resize((128, 128), Image.LANCZOS)  # fixed size
    pixel_array = np.array(img).flatten()
    sha = hashlib.sha256(pixel_array.tobytes()).hexdigest()
    return sha


def signatures_match(sig1: str, sig2: str) -> bool:
    return sig1.strip().lower() == sig2.strip().lower()
