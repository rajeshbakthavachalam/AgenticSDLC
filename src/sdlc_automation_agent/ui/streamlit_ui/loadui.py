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
        "isSubmitButtonClicked": False,
        "current_step": "requirements",
        "project_name": "",
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
        
       
        st.session_state["isSubmitButtonClicked"] = False

        # Input field for project name
        project_name = st.text_input("Enter the project name:")
        st.session_state["project_name"] = project_name

        # Multiline text area for requirements
        requirements_input = st.text_area(
            "Enter the requirements (each requirement should start with '- ').\nWrite each requirement on a new line:"
        )

        # Split input into a list of requirements
        requirements = [req.strip() for req in requirements_input.split("\n") if req.strip()]

        # Ensure each requirement starts with '- '
        requirements = ["- " + req if not req.startswith("- ") else req for req in requirements]
        st.session_state["requirements"] = requirements

        # Submit button
        if st.button("Submit"):
            if not project_name:
                st.error("Please enter a project name.")
            elif not requirements:
                st.error("Please enter at least one requirement.")
            else:
                st.success("Project details saved successfully!")
                
                st.session_state["isSubmitButtonClicked"] = True
                
                # Display the project details
                st.subheader("Project Details:")
                st.write(f"**Project Name:** {project_name}")
                st.subheader("Requirements:")
                for req in requirements:
                    st.write(req)

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