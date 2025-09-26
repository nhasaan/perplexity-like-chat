from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from services.data_connector_service import DataConnectorService

router = APIRouter()
data_service = DataConnectorService()

@router.get("/")
async def get_available_data_sources():
    """Get list of available data sources"""
    sources = [
        {
            "id": "google_ads",
            "name": "Google Ads Tag",
            "description": "Connect to Google Ads for audience insights and campaign data",
            "status": "available"
        },
        {
            "id": "facebook_pixel",
            "name": "Facebook Pixel",
            "description": "Connect to Facebook Pixel for behavioral data and retargeting",
            "status": "available"
        },
        {
            "id": "website",
            "name": "Website Analytics",
            "description": "Connect to website for general analytics and user behavior",
            "status": "available"
        }
    ]
    return {"sources": sources}

@router.post("/connect/{source_id}")
async def connect_data_source(source_id: str, connection_data: Dict[str, Any]):
    """Connect to a specific data source"""
    try:
        result = await data_service.connect_source(source_id, connection_data)
        return {
            "success": True,
            "source_id": source_id,
            "connection_id": result.get("connection_id"),
            "status": "connected"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/connections")
async def get_connections():
    """Get all active data source connections"""
    try:
        connections = await data_service.get_all_connections()
        return {"connections": connections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/disconnect/{connection_id}")
async def disconnect_data_source(connection_id: str):
    """Disconnect a data source"""
    try:
        await data_service.disconnect_source(connection_id)
        return {"success": True, "message": "Data source disconnected"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/data/{source_id}")
async def get_data_source_data(source_id: str):
    """Get data from a connected data source"""
    try:
        data = await data_service.get_source_data(source_id)
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
