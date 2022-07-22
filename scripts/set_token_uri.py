from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import (
    MAPPING_BREED_TO_IMAGE,
    OPEN_SEA_URL,
    get_account,
    get_breed,
)


def main():
    account = get_account()
    print(f"Working on {network.show_active()}.")
    advancedCollectible = AdvancedCollectible[-1]
    tokenIds = advancedCollectible.tokenCounter()
    print(f"You have {tokenIds} tokenIds.")
    for id in range(tokenIds):
        if not advancedCollectible.tokenURI(id).startswith("https://"):
            breed = get_breed(advancedCollectible.tokenIdToBreed(id))
            tx = advancedCollectible.setTokenURI(
                id,
                MAPPING_BREED_TO_IMAGE[breed],
                {"from": account},
            )
            tx.wait(1)
            print(
                f"Awesome, you can view your NFT at {OPEN_SEA_URL.format(advancedCollectible.address,id)}."
            )
