from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from services.campaign_service import CampaignService

router = APIRouter()
campaign_service = CampaignService()

@router.post("/generate")
async def generate_campaign(campaign_request: Dict[str, Any]):
    """Generate a campaign based on chat context and data sources"""
    try:
        campaign = await campaign_service.generate_campaign(
            campaign_request.get("message", ""),
            campaign_request.get("data_sources", []),
            campaign_request.get("channels", []),
            campaign_request.get("client_id", "default")
        )
        return {
            "success": True,
            "campaign": campaign
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/channels")
async def get_available_channels():
    """Get list of available campaign channels"""
    channels = [
        {
            "id": "email",
            "name": "Email",
            "description": "Direct email marketing campaigns",
            "status": "available"
        },
        {
            "id": "sms",
            "name": "SMS",
            "description": "Mobile SMS marketing campaigns",
            "status": "available"
        },
        {
            "id": "whatsapp",
            "name": "WhatsApp",
            "description": "WhatsApp messaging campaigns",
            "status": "available"
        },
        {
            "id": "push",
            "name": "Push Notifications",
            "description": "Mobile app push notification campaigns",
            "status": "available"
        }
    ]
    return {"channels": channels}

@router.post("/execute/{campaign_id}")
async def execute_campaign(campaign_id: str, execution_data: Dict[str, Any]):
    """Execute a generated campaign"""
    try:
        result = await campaign_service.execute_campaign(campaign_id, execution_data)
        return {
            "success": True,
            "execution_id": result.get("execution_id"),
            "status": "executed"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/history/{client_id}")
async def get_campaign_history(client_id: str):
    """Get campaign history for a client"""
    try:
        history = await campaign_service.get_campaign_history(client_id)
        return {"campaigns": history}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
