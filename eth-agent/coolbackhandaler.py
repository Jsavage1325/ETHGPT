from typing import Optional, Dict, Any

from dotenv import load_dotenv
from ai_helper import AIHelper
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

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Print out that we are entering a chain."""
        class_name = serialized["name"]
        st.markdown(f"> Entering new **{class_name}** chain...")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain."""
        st.markdown("> **Finished chain.**")

    def on_agent_action(
        self, action: AgentAction, color: Optional[str] = None, **kwargs: Any
    ) -> Any:
        """Run on agent action."""
        st.markdown(action.log)

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
            st.markdown(f"\n{observation_prefix}")
        st.markdown(output)
        if llm_prefix is not None:
            st.markdown(f"\n{llm_prefix}")

    def on_text(
        self,
        text: str,
        color: Optional[str] = None,
        end: str = "",
        **kwargs: Any,
    ) -> None:
        """Run when agent ends."""
        st.markdown(text)

    def on_agent_finish(
        self, finish: AgentFinish, color: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Run on agent end."""
        st.markdown(finish.log)


# load env
load_dotenv()

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
        helper.agent.run(
            {
                "input": user_input,
                "chat_history": [],
            }
        )

    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"]) - 1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
