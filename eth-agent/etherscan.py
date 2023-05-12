import requests


class EtherscanAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.etherscan.io/api"

    def _get(self, payload):
        payload["apikey"] = self.api_key
        response = requests.get(self.base_url, payload)
        return response.json()

    def get_contract_abi(self, address):
        payload = {
            "module": "contract",
            "action": "getabi",
            "address": address,
        }
        return self._get(payload)

    def get_source_code(self, address):
        payload = {
            "module": "contract",
            "action": "getsourcecode",
            "address": address,
        }
        return self._get(payload)

    def get_contract_events(self, address, event_name, topic0, topic1, block_no):
        payload = {
            "module": "logs",
            "action": "getLogs",
            "fromBlock": block_no,
            "toBlock": "latest",
            "address": address,
            "topic0": topic0,
            "topic1": topic1,
            "topic1_2_opr": "and",
        }
        return self._get(payload)

    def get_tx_receipt_status(self, txhash):
        payload = {
            "module": "transaction",
            "action": "gettxreceiptstatus",
            "txhash": txhash,
        }
        return self._get(payload)


def main():
    api_key = "6UDPM3QGPDEM7P4ZTQ5DEIKXA3KHGW1IBC"
    etherscan = EtherscanAPI(api_key)

    # Example of using the wrapper
    contract_address = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"

    abi = etherscan.get_contract_abi(contract_address)
    print("ABI:", abi)

    source_code = etherscan.get_source_code(contract_address)
    # print("Source code:", source_code)

    # Other functions can be called in a similar manner


if __name__ == "__main__":
    main()
