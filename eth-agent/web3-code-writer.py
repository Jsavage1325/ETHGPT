from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

import os

import re
from typing import Dict, List

# load env variables
from dotenv import load_dotenv

load_dotenv()


def extract_code_from_response(response: str) -> Dict[str, List[str]]:
    code_blocks = re.findall(r"```(?:python|bash)?\s*[\s\S]*?```", response)

    extracted_code = {"python": [], "bash": []}

    for code_block in code_blocks:
        code_type, code = re.match(
            r"```(python|bash)?\s*([\s\S]*?)```", code_block
        ).groups()
        code_type = code_type or "python"
        extracted_code[code_type].append(code.strip())

    return extracted_code


sys_message = """
you are a natural language to eth agent. 

execute commands using web3.py. 

my wallet is already setup and libaries are installed. and connected using infura

return single a python function called command to complete the task like,

```python

from web3 import Web3

# Connect to web3 using Infura
infura_url = "https://mainnet.infura.io/v3/f4149201e122477882ce3ec91ed8a37b"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Set the account address and private key
account_address = "<YOUR_ACCOUNT_ADDRESS>"
private_key = "<YOUR_ACCOUNT_PRIVATE_KEY>"

def function_to_complete_command():
```

"""


chat = ChatOpenAI(temperature=0)

system_message_prompt = SystemMessagePromptTemplate.from_template(sys_message)

human_template = "{text}"

human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)

# get a chat completion from the formatted messages
resp = chat(chat_prompt.format_prompt(text="send eth to spink.eth").to_messages())


code = extract_code_from_response(resp.content)

with open("test3.py", "w") as f:
    f.write("\n".join(code["python"]))
