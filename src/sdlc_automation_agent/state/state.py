from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated

class State(TypedDict):
    """
    Represents the structure of the state used in the graph

    """
    
    messages: Annotated[list, add_messages]