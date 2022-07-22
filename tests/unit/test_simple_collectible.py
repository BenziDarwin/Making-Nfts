from eth_account import Account
from brownie import SimpleCollectible, network, accounts
from scripts.helpful_scripts import LOCAL_ENVIRONMENTS, get_account
import pytest

imageURI = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
openSeaUrl = "https://testnets.opensea.io/assets/{}/{}"


def test_deploy_and_create():
    if network.show_active() not in LOCAL_ENVIRONMENTS:
        pytest.skip()
    else:
        account = accounts[0]
        simpleCollectible = SimpleCollectible.deploy({"from": account})
        tx = simpleCollectible.createCollectible(imageURI, {"from": account})
        tx.wait(1)
        assert (
            simpleCollectible.ownerOf(simpleCollectible.tokenCounter() - 1) == account
        )
