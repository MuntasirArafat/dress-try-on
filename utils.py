import requests


def download_image(url, path):
    response = requests.get(
        url,
        timeout=120
    )

    response.raise_for_status()

    with open(path, "wb") as f:
        f.write(response.content)

    return path
