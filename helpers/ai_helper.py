"""
This is an AI helper which will query the docs of required libraries and attempt to write valid code using them
"""
from retrieve_docs import LangchainDocSearch
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.agents import load_tools
from langchain.tools import Tool
from langchain import SerpAPIWrapper
from langchain.tools import tool

llm = OpenAI(temperature=0.0)

search = SerpAPIWrapper()

tools = [
    # Tool(
    #     name="Intermediate Answer",
    #     func=search.run,
    #     description="Useful for when you need to search langchain docs"
    # ),
    LangchainDocSearch()
]

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
print(agent.agent.llm_chain.prompt.template)
agent.run({'input': "Can you write python code to create a local vectorstore to store embeddings from a csv file? Return Python code only.", 'chat_history': []})