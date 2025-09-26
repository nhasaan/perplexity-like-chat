from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
import json
from services.connection_manager import ConnectionManager
from services.ai_service import AIService

router = APIRouter()
connection_manager = ConnectionManager()
ai_service = AIService()

@router.post("/message")
async def send_message(message_data: Dict[str, Any]):
    """Process a chat message and return AI response"""
    try:
        response = await ai_service.process_chat_message(
            message_data.get("message", ""),
            message_data.get("client_id", "default")
        )
        return {
            "success": True,
            "response": response,
            "timestamp": message_data.get("timestamp")
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/history/{client_id}")
async def get_chat_history(client_id: str):
    """Get chat history for a specific client"""
    try:
        history = await ai_service.get_chat_history(client_id)
        return {
            "success": True,
            "history": history
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.delete("/history/{client_id}")
async def clear_chat_history(client_id: str):
    """Clear chat history for a specific client"""
    try:
        await ai_service.clear_chat_history(client_id)
        return {"success": True}
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
