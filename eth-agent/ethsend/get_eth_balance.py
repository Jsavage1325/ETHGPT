from ethsend.EthTransferBase import EthTransferBase

class GetEthBalance(EthTransferBase):
    name = 'get_eth_balance'
    description = 'A tool to get balance of ethereum (ETH) using an ethereum address. Returns a numerical value of the amount of eth in the wallet.'

    def _run(self, wallet_address: str):
        """
        Attempts to send amount of eth to target address
        """
        # Get the ETH balance
        eth_balance = self.web3.eth.get_balance(wallet_address)

        # Convert the balance from Wei to Ether
        return self.web3.from_wei(eth_balance, 'ether')


    def _arun(self, address: str):
        """
        Gets the etherscan contract code
        """
        raise NotImplementedError()