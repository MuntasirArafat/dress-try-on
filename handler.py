import base64
import uuid

import runpod

from model import generate_tryon
from utils import download_image


def handler(job):
    """
    Input:

    {
      "input": {
        "person_url": "...",
        "garment_url": "...",
        "category": "tops"
      }
    }
    """

    try:
        job_input = job["input"]

        person_url = job_input["person_url"]
        garment_url = job_input["garment_url"]

        category = job_input.get("category", "tops")

        request_id = str(uuid.uuid4())

        person_path = f"/tmp/{request_id}_person.jpg"
        garment_path = f"/tmp/{request_id}_garment.jpg"

        download_image(person_url, person_path)
        download_image(garment_url, garment_path)

        output_path = generate_tryon(
            person_path=person_path,
            garment_path=garment_path,
            category=category,
        )

        with open(output_path, "rb") as f:
            image_bytes = f.read()

        return {
            "success": True,
            "image": base64.b64encode(image_bytes).decode("utf-8"),
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


runpod.serverless.start(
    {
        "handler": handler
    }
)
