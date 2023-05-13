from langchain.tools import BaseTool
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from typing import Optional

class OneInchContextProvider(BaseTool):
    name = "one_inch_context_provider"
    description = """Expert who will answer specific questions related to 1inch. 1inch is decentrilised exchange aggregator (DEX). 
                    1inch is able to split trades across multiple DEXs to get the best price for the user. 
                    1inch fusion allows users to execute swaps as limit orders with a variable exchange rate.
                    Return text or 1inch query."""

    def load_vector_store(self):
        """
        Loads the langchain vector store from pickle into a local file
        """
        embeddings = OpenAIEmbeddings()
        global vector_store
        vector_store = FAISS.load_local("1inch_faiss_index", embeddings)

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """
        Search the 1inch docs and return the most relevant pages content which we will use to feed to the model
        """
        self.load_vector_store()
        res = vector_store.similarity_search(query)
        if res:
            return query + res[0].page_content
    
    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("1inch_doc_search does not support async")
