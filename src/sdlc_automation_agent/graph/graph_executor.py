from src.sdlc_automation_agent.state.sdlc_state import SDLCState
from src.sdlc_automation_agent.cache.redis_cache import flush_redis_cache, save_state_to_redis, get_state_from_redis
import uuid
import src.sdlc_automation_agent.utils.constants as const

class GraphExecutor:
    def __init__(self, graph):
        self.graph = graph

    def get_thread(self, task_id):
        return {"configurable": {"thread_id": task_id}}
    
    def start_workflow(self, project_name: str):
        
        graph = self.graph
        
        flush_redis_cache()
        
        # Generate a unique task id
        task_id = f"sdlc-task-{uuid.uuid4().hex[:8]}"
        
        thread = self.get_thread(task_id)
        
        for event in graph.stream({"project_name": project_name},thread, stream_mode="values"):
           print(f"Event Received: {event}")
        
        current_state = graph.get_state(thread)
        
        save_state_to_redis(task_id, current_state)
        
        return {"task_id" : task_id, "state": current_state}
    
    
    def generate_stories(self, task_id:str, requirements: list[str]):
        saved_state = get_state_from_redis(task_id)
        if saved_state:
            saved_state['requirements'] = requirements
        
        return self.update_and_resume_graph(saved_state,task_id,"get_user_requirements")


    def graph_review_flow(self, task_id, status, feedback, review_type):
        saved_state = get_state_from_redis(task_id)
        
        if saved_state:
            if review_type == const.REVIEW_USER_STORIES:
                saved_state['user_stories_review_status'] = status
                saved_state['user_stories_feedback'] = feedback
                node_name = "review_user_stories"
            elif review_type == const.REVIEW_DESIGN_DOCUMENTS:
                saved_state['design_documents_review_status'] = status
                saved_state['design_documents_feedback'] = feedback
                node_name = "review_design_documents"
            else:
                raise ValueError(f"Unsupported review type: {review_type}")
            
        return self.update_and_resume_graph(saved_state,task_id,node_name)
        
    
    def update_and_resume_graph(self, saved_state,task_id, as_node):
        graph = self.graph
        thread = self.get_thread(task_id)
        
        graph.update_state(thread, saved_state, as_node=as_node)
        
         # Resume the graph
        state = None
        for event in graph.stream(None, thread, stream_mode="values"):
            print(f"Event Received: {event}")
            state = event
        
        # saving the state before asking the product owner for review
        current_state = graph.get_state(thread)
        save_state_to_redis(task_id, current_state)
        
        return {"task_id" : task_id, "state": state}


    def get_design_documents(self, task_id):
        saved_state = get_state_from_redis(task_id)
        return {"task_id" : task_id, "state": saved_state}
