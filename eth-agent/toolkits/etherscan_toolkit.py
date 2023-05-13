from __future__ import annotations

from typing import List

from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.tools import BaseTool
from etherscan.get_code import EtherScanGetContractCode
from etherscan.get_abi import EtherScanGetContractABI
from etherscan.get_tx_status import EtherScanGetTXStatus

class EtherScanToolkit(BaseToolkit):
    """Toolkit for interacting with Gmail."""

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
            EtherScanGetContractCode,
            EtherScanGetContractABI,
            EtherScanGetTXStatus
        ]
