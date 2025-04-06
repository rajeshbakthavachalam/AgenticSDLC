from src.sdlc_automation_agent.state.sdlc_state import SDLCState
from src.sdlc_automation_agent.cache.redis_cache import flush_redis_cache, save_state_to_redis, get_state_from_redis
import uuid

class GraphExecutor:
    def __init__(self, graph):
        self.graph = graph

    def start_workflow(self, project_name: str):
        
        graph = self.graph
        
        flush_redis_cache()
        
        # Generate a unique task id
        task_id = f"sdlc-task-{uuid.uuid4().hex[:8]}"
        
        thread = {"configurable": {"thread_id": task_id}}
        
        for event in graph.stream({"project_name": project_name},thread, stream_mode="values"):
           print(f"Event Received: {event}")
        
        current_state = graph.get_state(thread)
        
        save_state_to_redis(task_id, current_state)
        
        return {"task_id" : task_id, "state": current_state}
    
    
    def generate_stories(self, task_id:str, requirements: list[str]):
        graph = self.graph
        
        thread = {"configurable": {"thread_id": task_id}} 
        
        saved_state = get_state_from_redis(task_id)
        if saved_state:
            saved_state['requirements'] = requirements
        
        graph.update_state(thread, saved_state, as_node="get_user_requirements")
        
        # Resume the graph
        state = None
        for event in graph.stream(None, thread, stream_mode="values"):
            print(f"Event Received: {event}")
            state = event
        
        # saving the state before asking the product owner for review
        current_state = graph.get_state(thread)
        save_state_to_redis(task_id, current_state)
        
        return {"task_id" : task_id, "state": current_state}
