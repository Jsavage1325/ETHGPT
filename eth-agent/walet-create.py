import os
from web3 import Web3

INFURA_PROJECT_ID = "f4149201e122477882ce3ec91ed8a37b"
INFURA_URL = f"https://goerli.infura.io/v3/{INFURA_PROJECT_ID}"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

new_wallet = web3.eth.account.create()
wallet_address = new_wallet.address

balance_in_wei = web3.eth.get_balance(wallet_address)
balance_in_eth = web3.from_wei(balance_in_wei, "ether")

print(f"New Wallet Address: {wallet_address}")
print(f"Wallet Balance: {balance_in_eth} Ether")
