import os
import json
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from google.antigravity import Agent
from lumina_travel.agent import get_travel_agent_config

app = FastAPI(title="Lumina Travel - AI Trip Concierge")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for agent
agent_instance = None
agent_context_manager = None

class ChatRequest(BaseModel):
    message: str

@app.on_event("startup")
async def startup_event():
    global agent_instance, agent_context_manager
    # Set up app data dir inside workspace for persistence and clean logs
    app_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".antigravity_travel"))
    os.makedirs(app_data_dir, exist_ok=True)
    
    config = get_travel_agent_config(app_data_dir=app_data_dir)
    
    # Check for GEMINI_API_KEY
    if not os.environ.get("GEMINI_API_KEY"):
        print("WARNING: GEMINI_API_KEY is not set in environment or .env file.")
    
    # Initialize agent context manager
    agent_context_manager = Agent(config)
    agent_instance = await agent_context_manager.__aenter__()
    print("Lumina Travel Agent successfully initialized!")

@app.on_event("shutdown")
async def shutdown_event():
    global agent_context_manager
    if agent_context_manager:
        await agent_context_manager.__aexit__(None, None, None)
        print("Lumina Travel Agent shutdown.")

# Import active bookings global from tools to show in frontend
from lumina_travel.tools import execute_booking

@app.get("/api/bookings")
async def get_bookings():
    # Retrieve current bookings from the agent's ToolContext state if possible
    # For robust frontend visual representation, we can also extract from agent or fallback
    # In tools.py, bookings are saved in ToolContext, let's also read them
    # Since we run a single session, we can get active bookings from agent's state or from tool level
    # Let's inspect the agent's conversation tool state
    bookings = []
    if agent_instance and agent_instance.conversation:
        # We can look up active state from the tool context
        # But to be safe and ensure the API returns the correct list,
        # we can define a small helper or retrieve it.
        # Let's fetch it via conversation context or custom global
        pass
    
    # Let's check a global state we will maintain in tools.py
    # We will modify tools.py to maintain a global LIST for simple API access
    from lumina_travel import tools
    if hasattr(tools, "ACTIVE_BOOKINGS"):
        bookings = tools.ACTIVE_BOOKINGS
        
    return JSONResponse(content={"bookings": bookings})

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    if not os.environ.get("GEMINI_API_KEY"):
        async def api_key_error_generator():
            yield "data: " + json.dumps({
                "type": "error", 
                "content": "API Key Missing: Please set your GEMINI_API_KEY in the `.env` file to start chatting."
            }) + "\n\n"
        return StreamingResponse(api_key_error_generator(), media_type="text/event-stream")
        
    async def sse_generator():
        try:
            response = await agent_instance.chat(request.message)
            
            # 1. Stream thought process if present
            if hasattr(response, "thoughts") and response.thoughts:
                async for thought in response.thoughts:
                    yield "data: " + json.dumps({"type": "thought", "content": thought}) + "\n\n"
                    await asyncio.sleep(0.01) # Small sleep for smooth front-end streaming
            
            # 2. Stream final text chunks
            async for chunk in response:
                yield "data: " + json.dumps({"type": "content", "content": chunk}) + "\n\n"
                await asyncio.sleep(0.01)
                
            # 3. Stream updated bookings list to trigger frontend refresh
            from lumina_travel import tools
            bookings = getattr(tools, "ACTIVE_BOOKINGS", [])
            yield "data: " + json.dumps({"type": "bookings_update", "bookings": bookings}) + "\n\n"
            
        except Exception as e:
            yield "data: " + json.dumps({"type": "error", "content": str(e)}) + "\n\n"

    return StreamingResponse(sse_generator(), media_type="text/event-stream")

# Mount static files
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))
os.makedirs(static_dir, exist_ok=True)
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
