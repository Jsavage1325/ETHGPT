from typing import Optional, Dict, Any

# from dotenv import load_dotenv
from ai_helper import AIHelper
import streamlit as st
from streamlit_chat import message
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish


class StreamlitCallbackHandler(BaseCallbackHandler):
    """Callback Handler that prints to Streamlit."""

    def __init__(self, color: Optional[str] = None) -> None:
        """Initialize callback handler."""
        self.color = color

    # def on_chain_start(
    #     self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    # ) -> None:
    #     """Print out that we are entering a chain."""
    #     print('starting new chain')
    #     class_name = serialized["name"]
    #     st.markdown(f"> Entering new **{class_name}** chain...")

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        st.markdown(f"Querying {serialized['name']}.")

    # def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
    #     """Print out that we finished a chain."""
    #     print('ending chain')
    #     st.markdown("> **Finished chain.**")

    # def on_agent_action(
    #     self, action: AgentAction, color: Optional[str] = None, **kwargs: Any
    # ) -> Any:
    #     """Run on agent action."""
    #     print('starting agent action')
    #     st.markdown(action.log)

    # def on_tool_end(
    #     self,
    #     output: str,
    #     color: Optional[str] = None,
    #     observation_prefix: Optional[str] = None,
    #     llm_prefix: Optional[str] = None,
    #     **kwargs: Any,
    # ) -> None:
    #     """If not the final action, print out observation."""
    #     print('ending tool')
    #     if observation_prefix is not None:
    #         st.markdown(f"\n{observation_prefix}")
    #     st.markdown(output)
    #     if llm_prefix is not None:
    #         st.markdown(f"\n{llm_prefix}")

    # def on_text(
    #     self,
    #     text: str,
    #     color: Optional[str] = None,
    #     end: str = "",
    #     **kwargs: Any,
    # ) -> None:
    #     """Run when agent ends."""
    #     print('starting text?')
    #     st.markdown(text)

    def on_agent_finish(
        self, finish: AgentFinish, color: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Run on agent end."""
        print('agent finished')
        # st.markdown(finish.log)
        st.session_state["generated"] = [finish.log]


# load env
# load_dotenv()

if __name__ == "__main__":
    st.set_page_config(page_title="LangChain Demo", page_icon=":robot:")
    st.header("LangChain Demo")

    helper = AIHelper(StreamlitCallbackHandler())

    if "generated" not in st.session_state:
        st.session_state["generated"] = []

    if "past" not in st.session_state:
        st.session_state["past"] = []

    def get_text():
        input_text = st.text_input("You: ", "", key="input")
        return input_text

    user_input = get_text()

    if user_input:
        helper.run_query(user_input)

        # set output to the final output of the query
        # output = 'banana'

        # print(f'output: {output}')

        st.session_state.past.append(user_input)
        # st.session_state.generated.append(output)

    print(st)
    print(st.session_state)

    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"]) - 1, -1, -1):
            message(st.session_state["generated"][i])  # ), key=str(i))
            print(st.session_state["generated"])
            print(st.session_state["past"])
            message(
                st.session_state["past"][i], is_user=True
            )  # , key=str(i) + "_user")
