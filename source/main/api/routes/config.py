from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any
import os

router = APIRouter()

@router.get("/")
async def get_configuration() -> Dict[str, Any]:
    """
    Get application configuration and capabilities.
    Frontend calls this to understand what features are available.
    """
    try:
        # Check if real data sources are enabled
        use_real_data = os.getenv("USE_REAL_DATA_SOURCES", "false").lower() == "true"
        
        # Check which data sources are actually configured
        data_sources = []
        
        # Google Ads
        if use_real_data and all([
            os.getenv("GOOGLE_ADS_API_KEY"),
            os.getenv("GOOGLE_ADS_CUSTOMER_ID"),
            os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN")
        ]):
            data_sources.append({
                "id": "google_ads",
                "name": "Google Ads",
                "description": "Google Ads audience and campaign data",
                "available": True,
                "real_data": True
            })
        else:
            data_sources.append({
                "id": "google_ads",
                "name": "Google Ads",
                "description": "Google Ads audience and campaign data (Mock)",
                "available": True,
                "real_data": False
            })
        
        # Facebook Pixel
        if use_real_data and all([
            os.getenv("FACEBOOK_ACCESS_TOKEN"),
            os.getenv("FACEBOOK_PIXEL_ID")
        ]):
            data_sources.append({
                "id": "facebook_pixel",
                "name": "Facebook Pixel",
                "description": "Facebook Pixel events and audiences",
                "available": True,
                "real_data": True
            })
        else:
            data_sources.append({
                "id": "facebook_pixel",
                "name": "Facebook Pixel",
                "description": "Facebook Pixel events and audiences (Mock)",
                "available": True,
                "real_data": False
            })
        
        # Website Analytics
        if use_real_data and all([
            os.getenv("GOOGLE_ANALYTICS_CREDENTIALS_PATH"),
            os.getenv("GOOGLE_ANALYTICS_PROPERTY_ID")
        ]):
            data_sources.append({
                "id": "website",
                "name": "Website Analytics",
                "description": "Website traffic and behavior data",
                "available": True,
                "real_data": True
            })
        else:
            data_sources.append({
                "id": "website",
                "name": "Website Analytics",
                "description": "Website traffic and behavior data (Mock)",
                "available": True,
                "real_data": False
            })
        
        # Available channels
        channels = [
            {"id": "email", "name": "Email", "available": True},
            {"id": "sms", "name": "SMS", "available": True},
            {"id": "whatsapp", "name": "WhatsApp", "available": True},
            {"id": "push", "name": "Push Notifications", "available": True}
        ]
        
        # Feature flags based on backend configuration
        features = {
            "real_data_sources": use_real_data,
            "campaign_generation": True,
            "websocket_chat": True,
            "data_source_management": True,
            "campaign_execution": True
        }
        
        return {
            "success": True,
            "configuration": {
                "data_sources": data_sources,
                "channels": channels,
                "features": features,
                "app_info": {
                    "name": "Perplexity Chat",
                    "version": "1.0.0",
                    "environment": "production" if not os.getenv("DEBUG", "false").lower() == "true" else "development"
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")

@router.get("/health")
async def config_health():
    """Health check for configuration service"""
    return {"status": "healthy", "service": "config"}
