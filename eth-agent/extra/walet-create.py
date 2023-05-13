from eth_account import Account
import secrets
import json

priv = secrets.token_hex(32)
private_key = "0x" + priv
print("SAVE BUT DO NOT SHARE THIS:", private_key)
acct = Account.from_key(private_key)
print("Address:", acct.address)

# write all of the wallet data to a file as json
wallet_data = {"private_key": private_key, "address": acct.address}

with open("wallet.json", "w") as outfile:
    json.dump(wallet_data, outfile)

# load the wallet data from the file
with open("wallet.json", "r") as infile:
    wallet_data = json.load(infile)

private_key = wallet_data["private_key"]
