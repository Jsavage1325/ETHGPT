from langchain.tools import BaseTool
import pickle
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from typing import Optional
import faiss

class AirstackContextProvider(BaseTool):
    name = "airstack_context_provider"
    description = """Airstack expert who will tell you how to write GraphQL queries for Airstack.
                    Endpoints: Tokens,NFTs,Balances,Domains,Wallet,Socials,Transfers,NFT Sales,Collection Stats,Marketplace Stats
                    You will provide this expert with a summary of what you want to do.
                    Returns text or a GraphQL query."""

    def load_vector_store(self):
        """
        Loads the airstack vector store from pickle into a local file
        """
        global vector_store
        print([i for i in dir(faiss) if '__' not in i])
        vector_store = faiss.load_local('airstack_baby_faiss_index')
        # with open("airstack_baby_faiss_index/index.pkl", "rb") as f:
        #     vector_store, something_strange = pickle.load(f)
        #     print(vector_store)

    def _run(self, query: str) -> str:
        """
        Search the docs and return the most relevant pages content which we will use to feed to the model
        """
        self.load_vector_store()
        res = vector_store.similarity_search(query)
        if res:
            return res[0].page_content + res[1].page_content + res[2].page_content
    
    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("airstack_doc_search does not support async")