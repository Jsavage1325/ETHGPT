from langchain.tools import BaseTool
from EtherScanBase import EtherScanBase


class EtherScanGetContractABI(EtherScanBase):
    name = 'get_ether_contract_abi'
    desription = 'Gets the ABI for an ethereum contract using an address, where possible.'

    def _run(self, address: str):
        """
        Gets the etherscan contract code
        """
        payload = {
            "module": "contract",
            "action": "getsourcecode",
            "address": address,
        }
        return self._get(payload)
    