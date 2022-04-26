from brownie import FundMe, accounts, config, network, MockV3Aggregator
from scripts.helpful_scripts import deploy_mocks, get_account
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def deploy_fund_me():
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        # else if network is local development then we need to create mock
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        print(f"price feed address is {price_feed_address}")
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fund_me()
