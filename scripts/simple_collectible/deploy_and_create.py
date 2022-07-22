from brownie import SimpleCollectible
from scripts.helpful_scripts import get_account

imageURI = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
openSeaUrl = "https://testnets.opensea.io/assets/{}/{}"


def create_and_deploy():
    account = get_account()
    simpleCollectible = SimpleCollectible.deploy({"from": account})
    tx = simpleCollectible.createCollectible(imageURI, {"from": account})
    tx.wait(1)
    print(
        f"Collectible created!, you can check your nft from {openSeaUrl.format(simpleCollectible.address, simpleCollectible.tokenCounter() -1)}"
    )


def main():
    create_and_deploy()
