import os
from pathlib import Path

import requests
from brownie import AdvancedCollectible
from scripts.helpful_scripts import get_breed

PINATA_BASE_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS"
headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}


def main():
    advancedCollectible = AdvancedCollectible[-1]
    number_of_collectibles = advancedCollectible.tokenCounter()
    print(f"You have created {number_of_collectibles} collectibles!")
    for token_id in range(number_of_collectibles):
        breed = get_breed(advancedCollectible.tokenIdToBreed(token_id))
        image_name = breed.lower().replace("_", "-")
        file_path = f"./img/{image_name}.png"
        file_name = file_path.split("/")[-1:][0]
        upload_to_pinata(file_path, file_name)


def upload_to_pinata(_filePath, _filename):
    with Path(_filePath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            headers=headers,
            files={"file": (_filename, image_binary)},
        )
        print(response.json())
