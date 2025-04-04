from src.sdlc_automation_agent.state.sdlc_state import SDLCState, UserStories
from langchain_core.messages import SystemMessage

class ProjectRequirementNode:
    """
    Graph Node for the project requirements
    
    """
    
    def __init__(self, model):
        self.llm = model
        
    def get_user_requirements(self, state:SDLCState):
        """
            Get the user input for the project requirements
        """
        pass
        
    
    def generate_user_stories(self, state:SDLCState):
        """
            Auto generate the user stories based on the user requirements provided
        """
        project_name = state['project_name']
        requirements = state['requirements']
        feedback_reason = None
        
        prompt = f"""
        You are an expert in software development and requirements analysis. Based on the project name "{project_name}" and the following requirement:
        - {requirements}

        Please generate a user story in Markdown format. The user story should include:
        - A unique identifier
        - A title
        - A detailed description
        - Priority
        - Acceptance criteria

        {f"When creating this user story, please incorporate the following feedback about the requirements: {feedback_reason}" if feedback_reason else ""}

        Format the user story as a bullet point.
        """
        system_message = prompt.format(project_name= project_name, requirement= requirements)
        llm_with_structured = self.llm.with_structured_output(UserStories)
        response = llm_with_structured.invoke(system_message)
        state["user_stories"] = response
        return state
    
    