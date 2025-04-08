from src.sdlc_automation_agent.state.sdlc_state import SDLCState, UserStoryList
from langchain_core.messages import SystemMessage

class CodingNode:
    """
    Graph Node for the Coding
    
    """
    
    def __init__(self, model):
        self.llm = model
    
    def generate_code(self, state: SDLCState):
        pass
