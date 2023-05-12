from langchain.tools import BaseTool
from EtherScanBase import EtherScanBase


class EtherScanGetContractCode(EtherScanBase):
    name = 'get_ether_contract_code'
    desription = 'Gets the code for an ethereum contract using an address, where possible.'

    def _run(self, address: str):
        """
        Gets the etherscan contract code
        """
        payload = {
            "module": "contract",
            "action": "getabi",
            "address": address,
        }
        return self._get(payload)
    