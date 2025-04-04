import streamlit as st
from src.sdlc_automation_agent.state.sdlc_state import SDLCState, UserStories
import json


class DisplayResultStreamlit:
    def __init__(self, graph, project_name, requirements):
        self.graph = graph
        self.project_name = project_name
        self.requirements = requirements
                
                            
    def display_result_on_ui(self):
        graph = self.graph
        project_name = self.project_name
        requirements = self.requirements
        
        ## Display result on the UI
        try:    
            # Process user stories from the response
            response = graph.invoke({"project_name": project_name, "requirements": requirements})
            
            print(response)
            
            if "user_stories" in response:
                st.subheader("Generated User Stories")

               # Ensure user_stories is a list (even if it's a single object)
                user_stories = response["user_stories"]
                if not isinstance(user_stories, list):
                    user_stories = [user_stories]  # Convert single story to a list
        

                for idx, story in enumerate(user_stories):
                    unique_id = f"US-{idx+1:03}"  # Generating Unique Identifier (e.g., US-001, US-002)

                    with st.container():
                        st.markdown(f"##### {story.title} ({unique_id})")  # Title with Unique ID
                        st.write(f"**Priority:** {story.priority}")  # Priority Level
                        st.write(f"**Description:** {story.description}")
                        st.write(f"**Acceptance Criteria:**")
                        st.markdown(f"{story.acceptance_criteria}")  # Styled blockquote
                        st.divider()
                                            
        except Exception as e:
            st.error(f"Error generating results: {str(e)}")
            
            
        