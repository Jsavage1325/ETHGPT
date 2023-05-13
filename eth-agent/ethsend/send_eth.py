from ethsend.EthTransferBase import EthTransferBase

class EthSend(EthTransferBase):
    name = 'send_eth'
    description = 'A tool to send ethereum (ETH) via the smart contract, requires an address and an amount in the form 0xD245Fbe9F1F7cf8944528bA1CeD277272f0da061 and 0.001. Returns transaction id if successful'

    def _run(self, data: str):
        """
        Attempts to send amount of eth to target address
        """
        #get the nonce.  Prevents one from sending the transaction twice
        nonce = self.web3.eth.get_transaction_count(self.wallet_address)

        target_address = data.split(' and ')[0]
        amount = data.split(' and ')[1]

        #build a transaction in a dictionary
        tx = {
        'nonce': nonce,
        'to': target_address,
        'value': self.web3.to_wei(amount, 'ether'),
        'gas': 2000000,
        'gasPrice': self.web3.to_wei('50', 'gwei')
        }   
        #sign the transaction
        signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)

        #send transaction and return tx_hash
        return self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    def _arun(self, address: str):
        """
        Gets the etherscan contract code
        """
        raise NotImplementedError()