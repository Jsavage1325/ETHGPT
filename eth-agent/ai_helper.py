from tools.code.PythonCodeWriter import PythonCodeWriter
from experts.airstack_expert import AirstackContextProvider
from experts.langchain_expert import LangchainContextProvider
from SmartContractAnalysis import SmartContractAnalysis
from tools.etherscan.get_abi import EtherScanGetContractABI
from tools.etherscan.get_code import EtherScanGetContractCode
from tools.etherscan.get_tx_status import EtherScanGetTXStatus
from tools.ethsend.send_eth import EthSend
from tools.ethsend.get_eth_balance import GetEthBalance
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain import SerpAPIWrapper


class AIHelper:
    def __init__(self):
        self.llm = OpenAI(temperature=0.0)
        self.search = SerpAPIWrapper()

        self.tools = [
            PythonCodeWriter(),
            EthSend(),
            GetEthBalance(),
            LangchainContextProvider(),
            AirstackContextProvider(),
        ]

        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )

    def run_query(self, query):
        self.agent.run(
            {
                "input": query,
                "chat_history": [],
            }
        )


if __name__ == "__main__":
    helper = AIHelper()
    query = "Can you write a GraphQL query to get all NFTs owned by spink.eth?"
    helper.run_query(query)
