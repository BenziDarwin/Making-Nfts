import json
import requests
from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path


def create_metadata():
    advancedCollectible = AdvancedCollectible[-1]
    number_of_collectibles = advancedCollectible.tokenCounter()
    print(f"You have created {number_of_collectibles} collectibles!")
    for token_id in range(number_of_collectibles):
        breed = get_breed(advancedCollectible.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        collectibleMetadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists, delete it to overwrite it.")
        else:
            print(f"Creating json file {metadata_file_name}")
            collectibleMetadata["name"] = breed
            img_name = breed.lower().replace("_", "-")
            collectibleMetadata["description"] = f"An adorable {img_name} pup"
            file_path = f"./img/{img_name}.png"
            image_uri = upload_to_ipfs(file_path)
            collectibleMetadata["image"] = image_uri
            with Path(metadata_file_name).open("w") as file:
                json.dump(collectibleMetadata, file)
            upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(_filePath):
    with Path(_filePath).open("rb") as fp:
        image_binary = fp.read()
        # Upload to IPFS
        ipfs_url = "http://127.0.0.1:5001/api/v0/add"
        response = requests.post(ipfs_url, files={"file": image_binary}, timeout=60)
        ipfs_hash = response.json()["Hash"]
        filename = _filePath.split("/")[-1:][0]
        image_url = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_url)
        return image_url


def main():
    create_metadata()
