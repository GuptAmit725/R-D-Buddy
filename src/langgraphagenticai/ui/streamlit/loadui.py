import streamlit as st
import os
from src.langgraphagenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title=self.config.get_page_title(), layout="wide")
        st.header(self.config.get_page_title(), )
        st.session_state.timeframe = "" 
        st.session_state.IsFetchButtonClicked = False

        with st.sidebar:
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)
            if self.user_controls["selected_llm"] == "Gemini":
                model_options = self.config.get_gemini_options()
                self.user_controls["selected_gemini_model"] = st.selectbox("Select Model", model_options)
                self.user_controls["GEMINI_API_KEY"] = st.text_input("API Key", type="password")

            ##Use case selection
            selected_usecase = st.selectbox("Select Usecases", usecase_options)
            self.user_controls["selected_usecase"] = selected_usecase

            if self.user_controls["selected_usecase"] == "Chatbot With Tool":
                self.user_controls["CANDIDATE_SKILLS"] = st.text_input("CANDIDATE SKILLS", type="default")

                if not self.user_controls["CANDIDATE_SKILLS"]:
                    st.warning("Candidate skills are mandatory to provide.")
            
            if self.user_controls["selected_usecase"] == "Call or Put":
                st.subheader("Company news explorer")

                os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("TAVILY API KEY", type="password")
                self.user_controls["COMPANY_NAME"] = st.session_state["COMPANY_NAME"] = st.text_input("Company Name", type="default")
                with st.sidebar:
                    time_frame = st.selectbox(
                        "Select Time Frame",
                        ["Daily", "Weekly", "Monthly"],
                        index=0
                    )
                if st.button("Fetch News", use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame

            if self.user_controls["selected_usecase"] == "arXiv Tutor":
                st.subheader("Lets userstand research paper")
                self.user_controls["ARXIV_ID"] = st.session_state["ARXIV_ID"] = st.text_input("ARXIV ID", type="default")
                st.warning("Mandatory field: The arxiv id should be in the format 1234:8967")

        return self.user_controls