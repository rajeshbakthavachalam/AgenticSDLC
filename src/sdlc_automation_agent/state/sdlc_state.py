from pydantic import BaseModel, Field
from typing import TypedDict, Any, Dict, Literal, Optional
import json

    
class UserStories(BaseModel):
    id: int = Field(...,description="The unique identifier of the user story")
    title: str = Field(...,description="The title of the user story")
    description: str = Field(...,description="The description of the user story")
    priority: int = Field(...,description="The priority of the user story")
    acceptance_criteria: str = Field(...,description="The acceptance criteria of the user story")

class UserStoryList(BaseModel):
    user_stories: list[UserStories]
    
class SDLCState(TypedDict):
    """
    Represents the structure of the state used in the SDLC graph

    """    
    project_name: str
    requirements: list[str]
    user_stories: UserStoryList
    
    

    