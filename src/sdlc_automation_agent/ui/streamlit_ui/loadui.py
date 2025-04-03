import streamlit as st
import os
from datetime import date
from dotenv import load_dotenv

from langchain_core.messages import AIMessage, HumanMessage
from src.sdlc_automation_agent.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        load_dotenv()
        self.config = Config() # config
        self.user_controls = {}
        
    def initialize_session(self):
        return {
        "current_step": "requirements",
        "requirements": "",
        "user_stories": "",
        "po_feedback": "",
        "generated_code": "",
        "review_feedback": "",
        "decision": None
    }

    def load_streamlit_ui(self):
        st.set_page_config(page_title=self.config.get_page_title(), layout="wide")
        st.header(self.config.get_page_title())
        st.subheader("Let AI agents plan your SDLC journey",
                 divider="rainbow", anchor=False)
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False
       

        with st.sidebar:
            # Get options from config
            llm_options = self.config.get_llm_options()

            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == 'Groq':
                # Model selection
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
                # API key input
                os.environ["GROQ_API_KEY"] = self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API Key",
                                                                                                      type="password")
                # Validate API key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")
                    
            if self.user_controls["selected_llm"] == 'Gemini':
                # Model selection
                model_options = self.config.get_gemini_model_options()
                self.user_controls["selected_gemini_model"] = st.selectbox("Select Model", model_options)
                # API key input
                os.environ["GEMINI_API_KEY"] = self.user_controls["GEMINI_API_KEY"] = st.session_state["GEMINI_API_KEY"] = st.text_input("API Key",
                                                                                                      type="password",
                                                                                                      value=os.getenv("GEMINI_API_KEY", "")) 
                # Validate API key
                if not self.user_controls["GEMINI_API_KEY"]:
                    st.warning("⚠️ Please enter your GEMINI API key to proceed. Don't have? refer : https://ai.google.dev/gemini-api/docs/api-key ")
                   
            
            if "state" not in st.session_state:
                st.session_state.state = self.initialize_session()
            
        return self.user_controls