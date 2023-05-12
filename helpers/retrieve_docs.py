from langchain import PromptTemplate
from langchain.tools import BaseTool
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
import pickle
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from typing import Optional


llm = ChatOpenAI(temperature=0)

class LangchainDocSearch(BaseTool):
    name = "langchain_doc_search"
    description = "useful for when you need to answer questions about current events"

    # def __init__(self):
    #     """
    #     Here we initialise the langchain docs as a retriever
    #     """
    #     self.vector_store = None
    #     # To load the objects from the file:
    #     with open("vectorstore.pkl", "rb") as f:
    #         self.vector_store = pickle.load(f)
    #     print('Initialised.')
    #     # FAISS.load_local()

    def load_vector_store(self):
        """
        """
        global vector_store
        with open("vectorstore.pkl", "rb") as f:
            vector_store = pickle.load(f)

    def _run(self, query: str) -> str:
        """Use the tool."""
        return vector_store.similarity_search(query)
        # return 
        # return search.run(query)
    
    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

# # An example prompt with one input variable
# langchain_prompt = PromptTemplate(
#     input_variables=["question"],
#     template="Act as a Python developer, using langchain to create different tools and agents. Using your knowledge of Python and the lanchain docs can you tell me how to {question}."
# )
# langchain_prompt.format(question="query on the available endpoints")

lds = LangchainDocSearch()
lds.load_vector_store()
from pprint import pprint
similar_docs = lds._run('Load a CSV document')