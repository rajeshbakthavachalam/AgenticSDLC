import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI


class GeminiLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input
        
        
    def get_llm_model(self):
        try:
            gemini_api_key = self.user_controls_input['GEMINI_API_KEY']
            selected_gemini_model = self.user_controls_input['selected_gemini_model']
            
            llm = ChatGoogleGenerativeAI(api_key=gemini_api_key, model= selected_gemini_model)
        
        except Exception as e:
            raise ValueError(f"Error occured with Exception : {e}")
        
        return llm