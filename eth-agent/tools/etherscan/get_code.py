from tools.etherscan.EtherScanBase import EtherScanBase


class EtherScanGetContractCode(EtherScanBase):
    name: str = 'get_ether_contract_code'
    description: str = 'Gets the code for an ethereum contract using an address, where possible.'

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

    def _arun(self, address: str):
        """
        Gets the etherscan contract code
        """
        raise NotImplementedError()
    