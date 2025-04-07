from pydantic import BaseModel, Field
from typing import TypedDict, Any, Dict, Literal, Optional
import json
import src.sdlc_automation_agent.utils.constants as const

    
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
    current_node: str = const.PROJECT_INITILIZATION
    feedback_reason: str
    review_status: str
    
    
    
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        # Check if the object is any kind of Pydantic model
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        # Or check for specific classes if needed
        # if isinstance(obj, UserStories) or isinstance(obj, DesignDocument):
        #     return obj.model_dump()
        return super().default(obj)
    

    