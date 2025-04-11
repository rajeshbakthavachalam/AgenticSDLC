from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from functools import lru_cache
from src.dev_pilot.LLMS.groqllm import GroqLLM
from src.dev_pilot.LLMS.geminillm import GeminiLLM
from src.dev_pilot.graph.graph_builder import GraphBuilder
import uvicorn
from contextlib import asynccontextmanager



def load_app():
     uvicorn.run(app, host="0.0.0.0", port=8000)


class Settings:
    def __init__(self):
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        

@lru_cache()
def get_settings():
    return Settings()


def validate_api_keys(settings: Settings = Depends(get_settings)):
    required_keys = {
        'GEMINI_API_KEY': settings.GEMINI_API_KEY,
        'GROQ_API_KEY': settings.GROQ_API_KEY
    }
    
    missing_keys = [key for key, value in required_keys.items() if not value]
    if missing_keys:
        raise HTTPException(
            status_code=500,
            detail=f"Missing required API keys: {', '.join(missing_keys)}"
        )
    return settings

# Initialize the LLM and GraphBuilder instances once and store them in the app state
@asynccontextmanager
async def lifespan(app: FastAPI):
    get_settings()
    llm = GeminiLLM().get_llm()
    graph_builder = GraphBuilder(llm=llm)
    graph = graph_builder.setup_graph()
    app.state.llm = llm
    app.state.graph = graph
    yield
    # Clean up resources if needed
    app.state.llm = None
    app.state.graph = None

app = FastAPI(
    title="DevPilot API",
    description="AI-powered SDLC API using Langgraph",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to DevPilot API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }