import streamlit as st
from src.sdlc_automation_agent.state.sdlc_state import SDLCState, UserStoryList
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
            
            print(response)  # Debugging output

            if "user_stories" in response:
                st.divider()
                st.subheader("Generated User Stories")

                user_story_list = response["user_stories"]

                if isinstance(user_story_list, UserStoryList):
                    for story in user_story_list.user_stories:
                        unique_id = f"US-{story.id:03}"  # Generating Unique Identifier (e.g., US-001, US-002)

                        with st.container():
                            st.markdown(f"#### {story.title} ({unique_id})")
                            st.write(f"**Priority:** {story.priority}") 
                            st.write(f"**Description:** {story.description}")
                            st.write(f"**Acceptance Criteria:**")
                            st.markdown(story.acceptance_criteria.replace("\n", "<br>"), unsafe_allow_html=True)
                            st.divider()

        except Exception as e:
            st.error(f"❌ Error generating results: {str(e)}")
            
            
        