import os
import subprocess

import torch
from PIL import Image

MODEL = None

WEIGHTS_DIR = "/app/weights"
MODEL_FILE = f"{WEIGHTS_DIR}/model.safetensors"


def ensure_weights():
    """
    Download weights only if missing.
    """

    if os.path.exists(MODEL_FILE):
        return

    os.makedirs(WEIGHTS_DIR, exist_ok=True)

    subprocess.run(
        [
            "python",
            "scripts/download_weights.py",
            "--weights-dir",
            WEIGHTS_DIR,
        ],
        cwd="/app/fashn-vton",
        check=True,
    )


def load_model():
    global MODEL

    if MODEL is not None:
        return MODEL

    print("Downloading weights if needed...")
    ensure_weights()

    print("Loading FASHN VTON model...")

    from fashn_vton import TryOnPipeline

    MODEL = TryOnPipeline(
        weights_dir=WEIGHTS_DIR,
        torch_dtype=torch.float16,
    )

    return MODEL


def generate_tryon(
    person_path,
    garment_path,
    category="tops"
):
    model = load_model()

    person = Image.open(person_path).convert("RGB")
    garment = Image.open(garment_path).convert("RGB")

    result = model(
        person_image=person,
        garment_image=garment,
        category=category,
    )

    output_path = "/tmp/output.png"

    result.images[0].save(output_path)

    return output_path
