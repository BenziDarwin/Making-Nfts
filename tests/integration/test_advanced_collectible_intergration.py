from time import sleep
from brownie import network
from scripts.helpful_scripts import LOCAL_ENVIRONMENTS
import pytest
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible_intergration():
    # deploy the contract
    # create an NFT
    # get a random breed back
    # Arrange
    if network.show_active() in LOCAL_ENVIRONMENTS:
        pytest.skip("Only for intergration testing")
    # Act
    advancedCollectible, creation_transaction = deploy_and_create()
    while advancedCollectible.randomNumber() == 0:
        print("Getting collectible...")
        sleep(5)
    randomNumber = advancedCollectible.randomNumber()
    tokenId = advancedCollectible.tokenCounter() - 1
    # Assert
    assert advancedCollectible.tokenCounter() == 1
    assert advancedCollectible.tokenIdToBreed(tokenId) == randomNumber % 3
