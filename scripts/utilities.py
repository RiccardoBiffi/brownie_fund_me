from brownie import MockV3Aggregator, network, accounts, config
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
DECIMALS = 8
STARTING_PRICE = 2000 * 10**8


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]  # primo account offerto da Ganache
    else:
        return accounts.add(config["wallets"]["from_key"])


def get_price_feed_address(tx_account):
    # Passo l'address dell'oracolo da cui prendo il feed del prezzo (mock se locale su ganache)
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        # Deploiamo un mock
        print(f"Acrive network: {network.show_active()}")
        print("Deploying Mocks...")
        if len(MockV3Aggregator) == 0:
            MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": tx_account})
            print("Mocks deployed")

        price_feed_address = MockV3Aggregator[-1].address

    return price_feed_address
