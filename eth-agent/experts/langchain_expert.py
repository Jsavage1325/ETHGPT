import pickle
from typing import Optional

from langchain.callbacks.manager import (AsyncCallbackManagerForToolRun,
                                         CallbackManagerForToolRun)
from langchain.tools import BaseTool


class LangchainContextProvider(BaseTool):
    name = "langchain_context_provider"
    description = """Langchain expert who will tell you how to do specific things using langchain. 
                    You will provide this expert with a summary of what you want to do with the tool.
                    It will return a information on how to use the specific tool."""

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
            return res[0].page_content + res[1].page_content + res[2].page_content
    
    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("langchain_doc_search does not support async")