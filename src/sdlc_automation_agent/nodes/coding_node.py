from src.sdlc_automation_agent.state.sdlc_state import SDLCState, UserStoryList
from src.sdlc_automation_agent.utils.Utility import Utility

class CodingNode:
    """
    Graph Node for the Coding
    
    """
    
    def __init__(self, model):
        self.llm = model
        self.utility = Utility()
    
    ## ---- Code Generation ----- ##
    def generate_code(self, state: SDLCState):
        """
            Generates the code for the requirements in the design document
        """
        print("----- Generating the code ----")
        
        requirements = state.get('requirements', '')
        user_stories = state.get('user_stories', '')
        code_feedback = None
        security_feedback = None
        
        if 'code_generated' in state:
            code_feedback = state.get('code_review_comments','')
        
        if 'security_recommendations' in state:
            security_feedback = state.get('security_recommendations','')
        
        prompt = f"""
        Generate Python code based on the following SDLC state:

            Project Name: {state['project_name']}

            Requirements:
            {self.utility.format_list(requirements)}
            
            User Stories:
            {self.utility.format_user_stories(user_stories)}
            
            Functional Design Document:
            {state['design_documents']['functional']}

            Technical Design Document:
            {state['design_documents']['technical']}

            {f"When generating this code, please incorporate the following feedback: {code_feedback}" if code_feedback else ""}
            
            {f"Also generating this code, please incorporate the following security recommendations: {security_feedback}" if security_feedback else ""}
                         
            The generated Python code should include:

            1. **Comments for Requirements**: Add each requirement as a comment in the generated code.
            2. **User Stories Implementation**: Include placeholders for each user story, with its description and acceptance criteria as comments.
            3. **Functional Design Reference**: Incorporate the functional design document content as a comment in the relevant section.
            4. **Technical Design Reference**: Include the technical design document details in a comment under its section.
            5. **Modularity**: Structure the code to include placeholders for different functionalities derived from the SDLC state, with clear comments indicating where each functionality should be implemented.
            6. **Python Formatting**: The generated code should follow Python syntax and best practices.

            Ensure the output code is modular, well-commented, and ready for development.
        """
        response = self.llm.invoke(prompt)
        state['code_generated'] = response.content
        return state
        
    def code_review(self, state: SDLCState):
        return state
    
    def fix_code(self, state: SDLCState):
        pass
    
    def code_review_router(self, state: SDLCState):
        """
            Evaluates Code review is required or not.
        """
        return state.get("code_review_status", "approved")  # default to "approved" if not present
    
    ## ---- Security Review ----- ##
    def security_review_recommendations(self, state: SDLCState):
        """
            Performs security review of the code generated
        """
         # Get the generated code from the state
        code_generated = state.get('code_generated', '')

         # Create a prompt for the LLM to review the code for security concerns
        prompt = f"""
            You are a security expert. Please review the following Python code for potential security vulnerabilities:
            ```
            {code_generated}
            ```
            Focus on:
            1. Identifying potential security risks (e.g., SQL injection, XSS, insecure data handling).
            2. Providing recommendations to mitigate these risks.
            3. Highlighting any best practices that are missing.

            End your review with an explicit APPROVED or NEEDS_FEEDBACK status.
        """

         # Invoke the LLM to perform the security review
        response = self.llm.invoke(prompt)
        state["security_recommendations"] =  response.content
        return state
    
    def security_review(self, state: SDLCState):
        return state
    
    def fix_code_after_security_review(self, state: SDLCState):
        pass
    
    def security_review_router(self, state: SDLCState):
        """
            Security Code review is required or not.
        """
        return state.get("security_review_status", "approved")  # default to "approved" if not present
    
    ## ---- Test Cases ----- ##
    def write_test_cases(self, state: SDLCState):
        pass