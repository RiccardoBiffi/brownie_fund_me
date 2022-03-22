from brownie import FundMe
from scripts.utilities import get_account


def fund():
    address = get_account()
    fund_me = FundMe[-1]
    entrance_fee = fund_me.getEntranceFee()
    print(f"The current entrance fee is {entrance_fee}")
    print("Funding...")

    fund_me.fund({"from": address, "value": entrance_fee})


def withdraw():
    address = get_account()
    fund_me = FundMe[-1]
    print("Withdrawing...")

    fund_me.withdraw({"from": address})


def main():
    fund()
    withdraw()
