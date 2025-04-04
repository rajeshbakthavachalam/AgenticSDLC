from langgraph.graph import StateGraph,START, END, MessagesState
from src.sdlc_automation_agent.state.sdlc_state import SDLCState, UserStories
from src.sdlc_automation_agent.nodes.project_requirement_node import ProjectRequirementNode

class GraphBuilder:
    
    def __init__(self, llm):
        self.llm = llm
        self.graph_builder = StateGraph(SDLCState)
                
    
    def build_sdlc_graph(self):
        """
            Configure the graph by adding nodes, edges
        """
        
        self.project_requirement_node = ProjectRequirementNode(self.llm)
        
        ## Nodes
        self.graph_builder.add_node("get_user_requirements", self.project_requirement_node.get_user_requirements)
        self.graph_builder.add_node("generate_user_stories", self.project_requirement_node.generate_user_stories)
        
        ## Edges
        self.graph_builder.add_edge(START,"get_user_requirements")
        self.graph_builder.add_edge("get_user_requirements","generate_user_stories")
        self.graph_builder.add_edge("generate_user_stories",END)
        
        
    def setup_graph(self):
        """
        Sets up the graph
        """
        self.build_sdlc_graph()
        return self.graph_builder.compile()