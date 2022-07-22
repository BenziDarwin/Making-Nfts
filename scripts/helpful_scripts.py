from brownie import (
    accounts,
    network,
    config,
    AdvancedCollectible,
    Contract,
    LinkToken,
    VRFCoordinatorMock,
)
from web3 import Web3

LOCAL_ENVIRONMENTS = ["ganache-cli", "development"]
FORKED_ENVIRONMENTS = ["mainnet-fork-dev"]
OPEN_SEA_URL = "https://testnets.opensea.io/assets/{}/{}"
BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}
PINATA_GATEWAY_URL = "https://gateway.pinata.cloud/ipfs/"

MAPPING_BREED_TO_IMAGE = {
    "PUG": "https://ipfs.io/ipfs/QmUcno8d6hmws8U7ECtCF3753jh71tL17yaHJyfSVFEaD9?filename=1-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmbJpLAZQ4Cn2b8KCaf7Gg29ZzwEuoRCR6Lmd4hR4TMX6k?filename=0-SHIBA_INU.json",
    "ST_BERNARD": "",
}


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]


contract_to_mock = {"linkToken": LinkToken, "vrfCoordinator": VRFCoordinatorMock}


def get_account():
    if (
        network.show_active() in LOCAL_ENVIRONMENTS
        or network.show_active() in FORKED_ENVIRONMENTS
    ):
        account = accounts[0]
        return account
    else:
        account = accounts.add(config["wallets"]["key"])
        return account


def deploy_contract():
    account = get_account()
    if len(AdvancedCollectible) <= 0:
        advancedCollectible = AdvancedCollectible.deploy(
            get_contract("vrfCoordinator"),
            get_contract("linkToken"),
            config["networks"][network.show_active()]["keyHash"],
            config["networks"][network.show_active()]["fee"],
            {"from": account},
        )
    else:
        advancedCollectible = AdvancedCollectible[0]
    return advancedCollectible


def get_contract(contract_name):
    """
    This function will either:
        - Get an address from the config
        - Or deploy a Mock to use for a network that doesn't have the contract
    Args:
        contract_name (string): This is the name of the contract that we will get
        from the config or deploy
    Returns:
        brownie.network.contract.ProjectContract: This is the most recently deployed
        Contract of the type specified by a dictionary. This could either be a mock
        or a 'real' contract on a live network.
    """
    # link_token
    # LinkToken
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    """
    Use this script if you want to deploy mocks to a testnet
    """
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks...")
    account = get_account()
    print("Deploying Mock LinkToken...")
    link_token = LinkToken.deploy({"from": account})
    print(f"Link Token deployed to {link_token.address}")
    print("Deploying Mock VRF Coordinator...")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print(f"VRFCoordinator deployed to {vrf_coordinator.address}")
    print("All done!")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=Web3.toWei(0.3, "ether")
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("linkToken")
    funding_tx = link_token.transfer(contract_address, amount, {"from": account})
    funding_tx.wait(1)
    print(f"Funded {contract_address}")
    return funding_tx
