from get_creds import get_etherscan_api_key
import requests
from langchain.tools import BaseTool

class EtherScanBase(BaseTool):
    """
    Base class for EtherScan interactions
    """
    def get_creds(self):
        self.api_key = get_etherscan_api_key()
        self.base_url = "https://api.etherscan.io/api"

    def _get(self, payload):
        self.get_creds()
        payload["apikey"] = self.api_key
        response = requests.get(self.base_url, payload)
        return response.json()