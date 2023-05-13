from typing import Optional, Dict, Any

from dotenv import load_dotenv
from tools.code.PythonCodeWriter import PythonCodeWriter
from experts.airstack_expert import AirstackContextProvider
from experts.langchain_expert import LangchainContextProvider
from experts.aave_expert import AaveContextProvider
from tools.ethsend.send_eth import EthSend
from tools.ethsend.get_eth_balance import GetEthBalance
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, AgentType
from langchain import SerpAPIWrapper
import streamlit as st
from streamlit_chat import message
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish


class StreamlitCallbackHandler(BaseCallbackHandler):
    """Callback Handler that prints to Streamlit."""

    def __init__(self, color: Optional[str] = None) -> None:
        """Initialize callback handler."""
        self.color = color

    # Method definitions remain the same, replace all print statements with Streamlit's st.write()

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Print out that we are entering a chain."""
        class_name = serialized["name"]
        st.write(f"\n\n> Entering new {class_name} chain...")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain."""
        st.write("\n> Finished chain.")

    def on_agent_action(
        self, action: AgentAction, color: Optional[str] = None, **kwargs: Any
    ) -> Any:
        """Run on agent action."""
        st.write(action.log)

    def on_tool_end(
        self,
        output: str,
        color: Optional[str] = None,
        observation_prefix: Optional[str] = None,
        llm_prefix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """If not the final action, print out observation."""
        if observation_prefix is not None:
            st.write(f"\n{observation_prefix}")
        st.write(output)
        if llm_prefix is not None:
            st.write(f"\n{llm_prefix}")

    def on_text(
        self,
        text: str,
        color: Optional[str] = None,
        end: str = "",
        **kwargs: Any,
    ) -> None:
        """Run when agent ends."""
        st.write(text)

    def on_agent_finish(
        self, finish: AgentFinish, color: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Run on agent end."""
        st.write(finish.log)


# load env
load_dotenv()


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
            AaveContextProvider(),
        ]

        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            streaming=True,
            callbacks=[StreamlitCallbackHandler()],
        )

    def run_query(self, query):
        self.agent.run(
            {
                "input": query,
                "chat_history": [],
            }
        )


if __name__ == "__main__":
    st.set_page_config(page_title="LangChain Demo", page_icon=":robot:")
    st.header("LangChain Demo")

    helper = AIHelper()

    if "generated" not in st.session_state:
        st.session_state["generated"] = []

    if "past" not in st.session_state:
        st.session_state["past"] = []

    def get_text():
        input_text = st.text_input("You: ", "", key="input")
        return input_text

    user_input = get_text()

    if user_input:
        output = helper.run_query(user_input)

        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"]) - 1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
