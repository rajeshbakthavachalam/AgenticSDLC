from pydantic import BaseModel, Field
from typing import TypedDict, Any, Dict, Literal, Optional
import json

    
class UserStories(BaseModel):
    title: str = Field(...,description="The title of the user story")
    description: str = Field(...,description="The description of the user story")
    priority: int = Field(...,description="The priority of the user story")
    acceptance_criteria: str = Field(...,description="The acceptance criteria of the user story")
    
    
class SDLCState(TypedDict):
    """
    Represents the structure of the state used in the SDLC graph

    """    
    project_name: str
    user_stories: list[UserStories]
    
    

    