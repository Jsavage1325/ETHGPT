from datetime import datetime

import faiss
import pandas as pd
import requests
import streamlit as st
# load env
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.docstore import InMemoryDocstore
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import (CombinedMemory, ConversationBufferMemory,
                              ConversationSummaryMemory,
                              VectorStoreRetrieverMemory)
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS

load_dotenv()

from datetime import datetime

import faiss
from langchain.chains import ConversationChain
from langchain.docstore import InMemoryDocstore
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import (CombinedMemory, ConversationBufferMemory,
                              ConversationSummaryMemory,
                              VectorStoreRetrieverMemory)
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS

embeddings = OpenAIEmbeddings()
air_vectorstore = FAISS.load_local("airstack_faiss_index", embeddings)
retriver = air_vectorstore.as_retriever(search_kwargs=dict(k=1))
memory_air = VectorStoreRetrieverMemory(retriever=retriver, memory_key="airstack")

embeddings_uni = OpenAIEmbeddings()
uni_vectorstore = FAISS.load_local("uniswap_faiss_index", embeddings_uni)
retriver_uni = uni_vectorstore.as_retriever(search_kwargs=dict(k=1))
memory_uni = VectorStoreRetrieverMemory(retriever=retriver_uni, memory_key="uniswap")


conv_memory = ConversationBufferMemory(
    memory_key="chat_history_lines", input_key="input"
)

summary_memory = ConversationSummaryMemory(
    llm=OpenAI(temperature=0, model_name="gpt-4", max_tokens=3999), input_key="input"
)
# Combined
memory = CombinedMemory(memories=[conv_memory, summary_memory, memory_air, memory_uni])
_DEFAULT_TEMPLATE = """

you are are designed to help the developer, when a user asks a question, you should write the code to solve the problem and explain it as much as possible

airstack docs
{airstack}

uniswap docs
{uniswap}

Summary of conversation:
{history}
Current conversation:
{chat_history_lines}
Human: {input}
AI:"""
PROMPT = PromptTemplate(
    input_variables=["history", "input", "chat_history_lines", "airstack", "uniswap"],
    template=_DEFAULT_TEMPLATE,
)
llm = OpenAI(temperature=0)
conversation = ConversationChain(llm=llm, verbose=True, memory=memory, prompt=PROMPT)


def ai_magic(query: str):
    return conversation.run(query)


# Get your API key from CoinMarketCap and replace 'your_api_key' with it.
def get_data():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": "02ad7da5-f491-4b24-a32c-384ca799186b",
    }

    # Send a request to the CoinMarketCap API.
    response = requests.get(url, headers=headers)
    return response.json()


data = get_data()


# Extract the top 10 cryptocurrencies and their information.
def some_transforming(data):
    top_10_cryptos = []
    for crypto in data["data"][:10]:
        crypto_name = crypto["name"]
        crypto_symbol = crypto["symbol"]
        crypto_rank = crypto["cmc_rank"]
        crypto_price = crypto["quote"]["USD"]["price"]
        crypto_market_cap = crypto["quote"]["USD"]["market_cap"]
        crypto_volume_24h = crypto["quote"]["USD"]["volume_24h"]

        top_10_cryptos.append(
            (
                crypto_name,
                crypto_symbol,
                crypto_rank,
                crypto_price,
                crypto_market_cap,
                crypto_volume_24h,
            )
        )

    # Convert the data to a pandas DataFrame.
    df = pd.DataFrame(
        top_10_cryptos,
        columns=["Crypto", "Symbol", "Rank", "Price", "Market Cap", "24h Volume"],
    )

    # Format the numeric values for better readability.
    df["Price"] = df["Price"].apply(lambda x: f"${x:,.2f}")
    df["Market Cap"] = df["Market Cap"].apply(lambda x: f"${x:,.2f}")
    df["24h Volume"] = df["24h Volume"].apply(lambda x: f"${x:,.2f}")
    return df


df = some_transforming(data)

st.title("Some info about crypto!")
st.write(df)

# add an input for run_magic
user_input = st.text_input("Ask me anything about crypto!")

if user_input:
    st.markdown(f"> **User:** {user_input}")
    response = ai_magic(user_input)
    st.markdown(f"> **AI:** {response}")
