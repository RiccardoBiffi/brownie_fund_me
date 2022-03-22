from brownie import accounts, network, exceptions
import pytest
from scripts.utilities import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy import deploy_fund_me


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me_contract = deploy_fund_me()
    entrance_fee = fund_me_contract.getEntranceFee() + 100

    tx1 = fund_me_contract.fund({"from": account, "value": entrance_fee})
    tx1.wait(1)
    assert fund_me_contract.address_amount(account.address) == entrance_fee

    tx2 = fund_me_contract.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me_contract.address_amount(account.address) == 0


def test_only_owner_withdraws():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    fund_me_contract = deploy_fund_me()
    hacker = accounts.add()  # chiave privata generata casualmente
    with pytest.raises(exceptions.VirtualMachineError):
        tx1 = fund_me_contract.withdraw({"from": hacker})
        tx1.wait(1)
