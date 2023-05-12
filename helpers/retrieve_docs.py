from langchain.tools import BaseTool
import pickle
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from typing import Optional

class LangchainDocSearch(BaseTool):
    name = "langchain_doc_search"
    description = "Langchain expert who will tell you how to do specific things using langchain."

    def load_vector_store(self):
        """
        Loads the langchain vector store from pickle into a local file
        """
        global vector_store
        with open("helpers/langchain_vectorstore.pkl", "rb") as f:
            vector_store = pickle.load(f)

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """
        Search the docs and return the most relevant pages content which we will use to feed to the model
        """
        self.load_vector_store()
        res = vector_store.similarity_search(query)
        if res:
            return res[0].page_content, res[0].metadata['source']
    
    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("langchain_doc_search does not support async")
    
class AirStackDocSearch(BaseTool):
    name = "airstack_doc_search"
    description = "AirStack expert who will tell you how to do specific things using airstack."

    def load_vector_store(self):
        """
        Loads the airstack vector store from pickle into a local file
        """
        global vector_store
        with open("helpers/airstack_vectorstore.pkl", "rb") as f:
            vector_store = pickle.load(f)

    def _run(self, query: str) -> str:
        """
        Search the docs and return the most relevant pages content which we will use to feed to the model
        """
        self.load_vector_store()
        res = vector_store.similarity_search(query)
        if res:
            return res[0].page_content, res[0].metadata['source']
    
    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("airstack_doc_search does not support async")
