import streamlit as st
import json
from src.sdlc_automation_agent.ui.streamlit_ui.loadui import LoadStreamlitUI
from src.sdlc_automation_agent.LLMS.groqllm import GroqLLM
from src.sdlc_automation_agent.LLMS.geminillm import GeminiLLM
from src.sdlc_automation_agent.LLMS.openai_llm import OpenAILLM
from src.sdlc_automation_agent.graph.graph_builder import GraphBuilder
from src.sdlc_automation_agent.ui.streamlit_ui.display_result import DisplayResultStreamlit

# MAIN Function START
def load_app():
    """
    Loads and runs the Automation Agent application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while 
    implementing exception handling for robustness.
    """
   
    # Load UI
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return

    # Text input for user message
    if st.session_state["isSubmitButtonClicked"]:
        project_name = st.session_state["project_name"]
        requirements = st.session_state["requirements"]
    else:
        project_name = None
        requirements = None

    print(project_name,requirements)
    
    if project_name and requirements:
        print("--------Starting workflow----------")
        try:
            # Configure LLM 
            selectedLLM = user_input.get("selected_llm")
            model = None
            if selectedLLM == "Gemini":
                obj_llm_config = GeminiLLM(user_controls_input=user_input)
                model = obj_llm_config.get_llm_model()
            elif selectedLLM == "Groq":
                obj_llm_config = GroqLLM(user_controls_input=user_input)
                model = obj_llm_config.get_llm_model()
            elif selectedLLM == "OpenAI":
                obj_llm_config = OpenAILLM(user_controls_input=user_input)
                model = obj_llm_config.get_llm_model()
            
            if not model:
                st.error("Error: LLM model could not be initialized.")
                return
            
            
            ## Graph Builder
            graph_builder=GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph()
                DisplayResultStreamlit(graph,project_name,requirements).display_result_on_ui()
                # DisplayResultStreamlit(graph,user_message).test_llm_call()
            except Exception as e:
                st.error(f"Error: Graph setup failed - {e}")
                return
            
        except Exception as e:
             raise ValueError(f"Error occured with Exception : {e}")
         
            
            
