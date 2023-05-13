from web3 import Web3, Account
import json

infura_url = "https://goerli.infura.io/v3/f4149201e122477882ce3ec91ed8a37b"
web3 = Web3(Web3.HTTPProvider(infura_url))

#load the wallet data from the file
with open("wallet.json", "r") as infile:
    wallet_data = json.load(infile)
    
private_key = wallet_data["private_key"]

# Set the account address and private key
account = Account.from_key(private_key)

