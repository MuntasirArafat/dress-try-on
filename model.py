import torch
from PIL import Image

MODEL = None


def load_model():
    global MODEL

    if MODEL is not None:
        return MODEL

    print("Loading FASHN VTON model...")

    # Replace with actual repository imports
    from fashn_vton.pipeline import TryOnPipeline

    MODEL = TryOnPipeline(
        weights_dir="./weights",
        torch_dtype=torch.float16,
    )

    return MODEL


def generate_tryon(person_path, garment_path, category="tops"):
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
