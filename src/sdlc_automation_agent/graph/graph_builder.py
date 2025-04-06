from langgraph.graph import StateGraph,START, END, MessagesState
from src.sdlc_automation_agent.state.sdlc_state import SDLCState, UserStories
from src.sdlc_automation_agent.nodes.project_requirement_node import ProjectRequirementNode
from src.sdlc_automation_agent.nodes.design_document_node import DesingDocumentNode
from langgraph.checkpoint.memory import MemorySaver

class GraphBuilder:
    
    def __init__(self, llm):
        self.llm = llm
        self.graph_builder = StateGraph(SDLCState)
        self.memory = MemorySaver()
                
    
    def build_sdlc_graph(self):
        """
            Configure the graph by adding nodes, edges
        """
        
        self.project_requirement_node = ProjectRequirementNode(self.llm)
        self.design_document_node = DesingDocumentNode(self.llm)
        
        ## Nodes
        self.graph_builder.add_node("initialize_project", self.project_requirement_node.initialize_project)
        self.graph_builder.add_node("get_user_requirements", self.project_requirement_node.get_user_requirements)
        self.graph_builder.add_node("generate_user_stories", self.project_requirement_node.generate_user_stories)
        # self.graph_builder.add_node("review_user_stories", self.project_requirement_node.review_user_stories)
        # self.graph_builder.add_node("create_design_document", self.design_document_node.create_design_document)
        
        ## Edges
        self.graph_builder.add_edge(START,"initialize_project")
        self.graph_builder.add_edge("initialize_project","get_user_requirements")
        self.graph_builder.add_edge("get_user_requirements","generate_user_stories")
        self.graph_builder.add_edge("generate_user_stories",END)
        # self.graph_builder.add_edge("generate_user_stories","review_user_stories")
        # self.graph_builder.add_conditional_edges(
        #     "review_user_stories",
        #     self.project_requirement_node.review_user_stories_router,
        #     {
        #         "approved": "create_design_document",
        #         "feedback": "generate_user_stories"
        #     }
        # )
        # self.graph_builder.add_edge("create_design_document",END)
         
       
        
        
    # def setup_graph(self):
    #     """
    #     Sets up the graph
    #     """
    #     self.build_sdlc_graph()
    #     return self.graph_builder.compile(
    #         interrupt_before=[
    #             'generate_user_stories'
    #         ],checkpointer=self.memory
    #     )
        
             
    def setup_graph(self):
        """
        Sets up the graph
        """
        self.build_sdlc_graph()
        
        graph =self.graph_builder.compile(
            interrupt_before=[
                'get_user_requirements'
            ],checkpointer=self.memory
        )
        
        img_data = graph.get_graph().draw_mermaid_png()

        # ✅ Save the image to a file
        graph_path = "workflow_graph.png"
        with open(graph_path, "wb") as f:
            f.write(img_data)
            
        return graph