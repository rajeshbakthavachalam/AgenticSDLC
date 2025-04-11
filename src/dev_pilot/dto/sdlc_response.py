from pydantic import BaseModel
from typing import Optional
from src.dev_pilot.state.sdlc_state import SDLCState
from typing import Dict, Any

class SDLCResponse(BaseModel):
    status: str
    message: str
    error: Optional[str] = None
    task_id: Optional[str] = None
    state: Optional[Dict[str, Any]] = None