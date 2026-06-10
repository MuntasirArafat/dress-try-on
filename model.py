import os
import subprocess
import traceback

import torch
from PIL import Image

MODEL = None

WEIGHTS_DIR = "/app/weights"
MODEL_FILE = f"{WEIGHTS_DIR}/model.safetensors"


def ensure_weights():
    if os.path.exists(MODEL_FILE):
        print("Weights already present")
        return

    os.makedirs(WEIGHTS_DIR, exist_ok=True)

    print("Downloading weights...")

    result = subprocess.run(
        [
            "python",
            "scripts/download_weights.py",
            "--weights-dir",
            WEIGHTS_DIR
        ],
        cwd="/app/fashn-vton",
        capture_output=True,
        text=True
    )

    print("DOWNLOAD STDOUT:")
    print(result.stdout)

    print("DOWNLOAD STDERR:")
    print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(
            f"""
Weight download failed

STDOUT:
{result.stdout}

STDERR:
{result.stderr}
"""
        )


def load_model():
    global MODEL

    if MODEL is not None:
        return MODEL

    ensure_weights()

    print("Loading FASHN VTON model...")

    from fashn_vton import TryOnPipeline

    MODEL = TryOnPipeline(
        weights_dir=WEIGHTS_DIR,
        torch_dtype=torch.float16
    )

    print("Model loaded")

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
        category=category
    )

    output_path = "/tmp/output.png"

    result.images[0].save(output_path)

    return output_path
