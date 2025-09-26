from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import asyncio
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

from api.routes import chat, data_sources, campaigns, config
from services.ai_service import AIService
from services.connection_manager import ConnectionManager
from models.database import init_db

# Load environment variables from orchestrate folder
env_path = os.path.join(os.path.dirname(__file__), '../../orchestrate/main/.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()  # Fallback to default .env location

app = FastAPI(
    title="Perplexity Chat API",
    description="AI-powered marketing campaign orchestration platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ai_service = AIService()
connection_manager = ConnectionManager()

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(data_sources.router, prefix="/api/data-sources", tags=["data-sources"])
app.include_router(campaigns.router, prefix="/api/campaigns", tags=["campaigns"])
app.include_router(config.router, prefix="/api/config", tags=["config"])

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await connection_manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "chat_message":
                # Process chat message with AI
                response = await ai_service.process_chat_message(
                    message_data.get("message", ""),
                    client_id
                )
                
                # Stream response back to client
                await connection_manager.send_personal_message(
                    json.dumps({
                        "type": "ai_response",
                        "content": response,
                        "timestamp": message_data.get("timestamp")
                    }),
                    client_id
                )
                
    except WebSocketDisconnect:
        connection_manager.disconnect(client_id)

@app.get("/")
async def root():
    return {"message": "Perplexity Chat API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "perplexity-chat"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
