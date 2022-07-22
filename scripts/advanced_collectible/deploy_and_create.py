from time import sleep
from scripts.helpful_scripts import fund_with_link, get_account, deploy_contract


def deploy_and_create():
    account = get_account()
    advancedCollectible = deploy_contract()
    fund_with_link(advancedCollectible.address)
    tx = advancedCollectible.createCollectible({"from": account})
    tx.wait(1)

    while advancedCollectible.randomNumber() == 0:
        print("Getting collectible...")
        sleep(5)
    print(advancedCollectible.randomNumber())
    return advancedCollectible, tx


def set_token_URI():
    account = get_account()
    advancedCollectible = deploy_contract()
    tokenId = advancedCollectible.tokenCounter() - 1


def main():
    deploy_and_create()
