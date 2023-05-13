from typing import Any, Dict, Optional

import streamlit as st
# from dotenv import load_dotenv
from ai_helper import AIHelper
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentFinish
from streamlit_chat import message


class StreamlitCallbackHandler(BaseCallbackHandler):
    """Callback Handler that prints to Streamlit."""

    def __init__(self, color: Optional[str] = None) -> None:
        """Initialize callback handler."""
        self.color = color
        self.status_text = st.empty()
        self.sources = st.empty()

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        # self.disappearing_info_message(f"Asking {serialized['name']}: {input_str}")
        # self.status_text = st.info(f"Asking {serialized['name']}: {input_str}", icon="ℹ️")
        self.status_text = st.text(f"ℹ️ Asking {serialized['name']}: {input_str}")

    def on_tool_end(
        self,
        output: str,
        color: Optional[str] = None,
        observation_prefix: Optional[str] = None,
        llm_prefix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """If not the final action, print out observation."""
        # self.disappearing_info_message(f'Finished asking {output}.')
        try:
            sources = output.split('|||')[1].split(',')
            if len(st.session_state["sources"]) > len(st.session_state['generated']):
                st.session_state["sources"][-1] += sources
            else:
                st.session_state["sources"].append(sources)
        except:
            pass
        self.status_text = st.text(f'ℹ️ Finished asking tool.')

    def on_agent_finish(
        self, finish: AgentFinish, color: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Run on agent end."""
        st.session_state["generated"].append(finish.log.split('Final Answer:')[1])
        for _ in range(100):
            self.status_text.empty()

    # def format_sources(self, sources):
    #     formatted_string = ""
    #     for source in sources:
    #         formatted_string += f'<a href="{source}">{source}</a>'
    #         # formatted_string += f"[{source}]({source})\n"
    #     return formatted_string



if __name__ == "__main__":
    st.set_page_config(page_title="ETHGPT", page_icon=":robot:")
    st.header("ETHGPT")

    sch = StreamlitCallbackHandler()

    helper = AIHelper(sch)

    if "generated" not in st.session_state:
        st.session_state["generated"] = []

    if "past" not in st.session_state:
        st.session_state["past"] = []

    if "sources" not in st.session_state:
        st.session_state["sources"] = []

    def get_text():
        input_text = st.text_input("You: ", "", key="input")
        return input_text

    user_input = get_text()

    if user_input:
        helper.run_query(user_input)

        st.session_state.past.append(user_input)

    if st.session_state["generated"]:
        # Add empty sources if no soures detected
        if len(st.session_state["sources"]) < len(st.session_state["generated"]):
            st.session_state["sources"].append([])
        # For reply in generated reply
        for i in range(len(st.session_state["generated"]) - 1, -1, -1):
            # Add generated reply to AI chat
            if st.session_state["sources"][i]:
                message(st.session_state["generated"][i] + '\n\nSources:\n' + '\n'.join(st.session_state["sources"][i]))  # ), key=str(i))
            else:
                message(st.session_state["generated"][i])  # ), key=str(i))
            
            # Add generated reply to human chat
            message(
                st.session_state["past"][i], is_user=True
            )  # , key=str(i) + "_user")
