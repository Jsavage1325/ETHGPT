from experts import AirstackContextProvider, LangchainContextProvider, AaveContextProvider, OneInchContextProvider, GnosisContextProvider, UniswapContextProvider
from tools.ethsend import EthSend, GetEthBalance
from tools.code import PythonCodeWriter
from tools.etherscan import EtherScanGetContractABI, EtherScanGetContractCode, EtherScanGetTXStatus
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, AgentType
from langchain import SerpAPIWrapper

class AIHelper:
    def __init__(self):
        self.llm = OpenAI(temperature=0.0)
        self.search = SerpAPIWrapper()

        self.tools = [
            EtherScanGetContractABI(),
            EtherScanGetContractCode(),
            EtherScanGetTXStatus(),
            PythonCodeWriter(),
            EthSend(),
            GetEthBalance(),
            LangchainContextProvider(),
            AirstackContextProvider(),
            AaveContextProvider(),
            OneInchContextProvider(),
            GnosisContextProvider(),
            UniswapContextProvider(),
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
    query = "What is the balance of spink.eth?"
    helper.run_query(query)
