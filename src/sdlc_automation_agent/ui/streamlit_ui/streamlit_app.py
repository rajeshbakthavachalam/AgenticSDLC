import streamlit as st
import json
from src.sdlc_automation_agent.LLMS.groqllm import GroqLLM
from src.sdlc_automation_agent.LLMS.geminillm import GeminiLLM
from src.sdlc_automation_agent.LLMS.openai_llm import OpenAILLM
from src.sdlc_automation_agent.graph.graph_builder import GraphBuilder
from src.sdlc_automation_agent.ui.uiconfigfile import Config
import src.sdlc_automation_agent.utils.constants as const
from src.sdlc_automation_agent.graph.graph_executor import GraphExecutor
from src.sdlc_automation_agent.state.sdlc_state import SDLCState, UserStoryList
import os


def initialize_session():
    st.session_state.stage = const.PROJECT_INITILIZATION
    st.session_state.project_name = ""
    st.session_state.requirements = ""
    st.session_state.task_id = ""
    st.session_state.state = {}
    st.session_state.show_review_section = True  # flag to show/hide review section


def load_sidebar_ui(config):
    user_controls = {}
    with st.sidebar:
        # Get options from config
        llm_options = config.get_llm_options()
        # LLM selection
        user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)
        if user_controls["selected_llm"] == 'Groq':
            model_options = config.get_groq_model_options()
            user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
            os.environ["GROQ_API_KEY"] = user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input(
                "API Key", type="password", value=os.getenv("GROQ_API_KEY", "")
            )
            if not user_controls["GROQ_API_KEY"]:
                st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")
        if user_controls["selected_llm"] == 'Gemini':
            model_options = config.get_gemini_model_options()
            user_controls["selected_gemini_model"] = st.selectbox("Select Model", model_options)
            os.environ["GEMINI_API_KEY"] = user_controls["GEMINI_API_KEY"] = st.session_state["GEMINI_API_KEY"] = st.text_input(
                "API Key", type="password", value=os.getenv("GEMINI_API_KEY", "")
            )
            if not user_controls["GEMINI_API_KEY"]:
                st.warning("⚠️ Please enter your GEMINI API key to proceed. Don't have? refer : https://ai.google.dev/gemini-api/docs/api-key ")
        if user_controls["selected_llm"] == 'OpenAI':
            model_options = config.get_openai_model_options()
            user_controls["selected_openai_model"] = st.selectbox("Select Model", model_options)
            os.environ["OPENAI_API_KEY"] = user_controls["OPENAI_API_KEY"] = st.session_state["OPENAI_API_KEY"] = st.text_input(
                "API Key", type="password", value=os.getenv("OPENAI_API_KEY", "")
            )
            if not user_controls["OPENAI_API_KEY"]:
                st.warning("⚠️ Please enter your OPENAI API key to proceed. Don't have? refer : https://ai.google.dev/gemini-api/docs/api-key ")
    return user_controls


def load_streamlit_ui(config):
    st.set_page_config(page_title=config.get_page_title(), layout="wide")
    st.header(config.get_page_title())
    st.subheader("Let AI agents plan your SDLC journey", divider="rainbow", anchor=False)
    user_controls = load_sidebar_ui(config)
    return user_controls


## Main Entry Point    
def load_app():
    """
    Main entry point for the Streamlit app using tab-based UI.
    """
    config = Config()
    if 'stage' not in st.session_state:
        initialize_session()

    user_input = load_streamlit_ui(config)
    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return

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
        graph_builder = GraphBuilder(model)
        try:
            graph = graph_builder.setup_graph()
            graph_executor = GraphExecutor(graph)
        except Exception as e:
            st.error(f"Error: Graph setup failed - {e}")
            return

        # Create tabs for different stages
        tabs = st.tabs(["Project Requirement", "User Stories", "Design Documents", "Other Stages"])

        # ---------------- Tab 1: Project Requirement ----------------
        with tabs[0]:
            st.header("Project Requirement")
            project_name = st.text_input("Enter the project name:", value=st.session_state.get("project_name", ""))
            st.session_state.project_name = project_name

            if st.session_state.stage == const.PROJECT_INITILIZATION:
                if st.button("🚀 Let's Start"):
                    if not project_name:
                        st.error("Please enter a project name.")
                        st.stop()
                    graph_response = graph_executor.start_workflow(project_name)
                    st.session_state.task_id = graph_response["task_id"]
                    st.session_state.state = graph_response["state"]
                    st.session_state.project_name = project_name
                    st.session_state.stage = const.REQUIREMENT_COLLECTION
                    st.rerun()

            # If stage has progressed beyond initialization, show requirements input and details.
            if st.session_state.stage in [const.REQUIREMENT_COLLECTION, const.GENERATE_USER_STORIES, const.CREATE_DESIGN_DOC]:
                requirements_input = st.text_area(
                    "Enter the requirements. Write each requirement on a new line:",
                    value="\n".join(st.session_state.get("requirements", []))
                )
                if st.button("Submit Requirements"):
                    requirements = [req.strip() for req in requirements_input.split("\n") if req.strip()]
                    st.session_state.requirements = requirements
                    if not requirements:
                        st.error("Please enter at least one requirement.")
                    else:
                        st.success("Project details saved successfully!")
                        st.subheader("Project Details:")
                        st.write(f"**Project Name:** {st.session_state.project_name}")
                        st.subheader("Requirements:")
                        for req in requirements:
                            st.write(req)
                        graph_response = graph_executor.generate_stories(st.session_state.task_id, requirements)
                        st.session_state.state = graph_response["state"]
                        st.session_state.stage = const.GENERATE_USER_STORIES
                        st.rerun()

        # ---------------- Tab 2: User Stories ----------------
        with tabs[1]:
            st.header("User Stories")
            if "user_stories" in st.session_state.state:
                user_story_list = st.session_state.state["user_stories"]
                st.divider()
                st.subheader("Generated User Stories")
                if isinstance(user_story_list, UserStoryList):
                    for story in user_story_list.user_stories:
                        unique_id = f"US-{story.id:03}"
                        with st.container():
                            st.markdown(f"#### {story.title} ({unique_id})")
                            st.write(f"**Priority:** {story.priority}")
                            st.write(f"**Description:** {story.description}")
                            st.write(f"**Acceptance Criteria:**")
                            st.markdown(story.acceptance_criteria.replace("\n", "<br>"), unsafe_allow_html=True)
                            st.divider()

            # If still in review stage, show review UI.
            if st.session_state.stage == const.GENERATE_USER_STORIES and st.session_state.get("show_review_section", True):
                st.subheader("Review User Stories")
                feedback_text = st.text_area("Provide feedback for improving the user stories (optional):")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Approve"):
                        st.success("✅ User stories approved.")
                        st.session_state.show_review_section = False
                        graph_response = graph_executor.review_user_stories(
                            st.session_state.task_id, status="approved", feedback=None
                        )
                        st.session_state.state = graph_response["state"]
                        st.session_state.stage = const.CREATE_DESIGN_DOC
                        st.rerun()
                with col2:
                    if st.button("✍️ Give Feedback"):
                        if not feedback_text.strip():
                            st.warning("⚠️ Please enter feedback before submitting.")
                        else:
                            st.info("🔄 Sending feedback to revise user stories.")
                            graph_response = graph_executor.review_user_stories(
                                st.session_state.task_id, status="feedback", feedback=feedback_text.strip()
                            )
                            st.session_state.state = graph_response["state"]
                            st.session_state.stage = const.GENERATE_USER_STORIES
                            st.rerun()
            else:
                st.info("User stories have been reviewed or are not yet generated.")

        # ---------------- Tab 3: Design Documents ----------------
        with tabs[2]:
            st.header("Design Documents")
            if st.session_state.stage == const.CREATE_DESIGN_DOC:
                st.subheader("Design Document")
                design_response = st.session_state.state.get("design_document", "Design document is being generated...")
                st.write(design_response)
            else:
                st.info("Design document generation pending or not reached yet.")

        # ---------------- Tab 4: Other Stages ----------------
        with tabs[3]:
            st.header("Other Stages")
            st.info("Future stages will be displayed here.")

    except Exception as e:
        raise ValueError(f"Error occured with Exception : {e}")