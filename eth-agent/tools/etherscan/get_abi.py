from tools.etherscan.EtherScanBase import EtherScanBase


class EtherScanGetContractABI(EtherScanBase):
    name = 'get_ether_contract_abi'
    description = 'Gets the ABI for an ethereum contract using an address, where possible.'
    

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

    def _arun(self, address: str):
        """
        Gets the etherscan contract code
        """
        raise NotImplementedError()
    