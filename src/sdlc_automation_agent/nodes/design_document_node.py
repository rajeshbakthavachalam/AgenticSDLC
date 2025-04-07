from src.sdlc_automation_agent.state.sdlc_state import SDLCState, UserStoryList
from langchain_core.messages import SystemMessage

class DesingDocumentNode:
    """
    Graph Node for the Desing Documents
    
    """
    
    def __init__(self, model):
        self.llm = model
    
    def create_design_document(self, state: SDLCState):
        pass