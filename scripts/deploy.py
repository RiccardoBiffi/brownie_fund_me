import time
from brownie import FundMe, accounts, network, config
from scripts.utilities import *


def deploy_fund_me():
    account = get_account()
    price_feed_address = get_price_feed_address(account)

    # Specificare sempre l'address nelle transazioni (ie accounts)
    # Pubblico il sorgente su Etherscan se non siamo in dev
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(f"Contratto deployato all'address {fund_me.address} con successo!")
    time.sleep(1)

    return fund_me


def main():
    deploy_fund_me()
