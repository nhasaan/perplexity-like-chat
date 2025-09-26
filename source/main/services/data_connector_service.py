from typing import Dict, List, Any
import asyncio
import json
from datetime import datetime
import os
from .real_data_connectors import RealDataConnectorService

class DataConnectorService:
    def __init__(self):
        self.connections: Dict[str, Dict] = {}
        self.real_connector_service = RealDataConnectorService()
        self.use_real_data = os.getenv("USE_REAL_DATA_SOURCES", "false").lower() == "true"
        self.mock_data = {
            "google_ads": {
                "audiences": [
                    {"name": "High Value Customers", "size": 15420, "engagement": 0.85},
                    {"name": "Cart Abandoners", "size": 8930, "engagement": 0.42},
                    {"name": "Recent Purchasers", "size": 2340, "engagement": 0.91}
                ],
                "campaigns": [
                    {"name": "Brand Awareness", "impressions": 125000, "clicks": 3200, "ctr": 0.0256},
                    {"name": "Retargeting", "impressions": 45000, "clicks": 1800, "ctr": 0.04}
                ]
            },
            "facebook_pixel": {
                "events": [
                    {"event": "PageView", "count": 125000, "conversion_rate": 0.12},
                    {"event": "AddToCart", "count": 15600, "conversion_rate": 0.08},
                    {"event": "Purchase", "count": 1248, "conversion_rate": 0.15}
                ],
                "audiences": [
                    {"name": "Lookalike 1%", "size": 45000, "similarity": 0.95},
                    {"name": "Custom Audience", "size": 8900, "similarity": 0.88}
                ]
            },
            "website": {
                "analytics": {
                    "sessions": 45600,
                    "bounce_rate": 0.35,
                    "avg_session_duration": 180,
                    "conversion_rate": 0.08
                },
                "traffic_sources": [
                    {"source": "Organic", "percentage": 45},
                    {"source": "Direct", "percentage": 25},
                    {"source": "Social", "percentage": 20},
                    {"source": "Paid", "percentage": 10}
                ]
            }
        }
    
    async def connect_source(self, source_id: str, connection_data: Dict[str, Any]) -> Dict[str, Any]:
        """Connect to a data source"""
        connection_id = f"{source_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if self.use_real_data:
            # Try real data source connection
            try:
                if source_id == "google_ads":
                    success = await self.real_connector_service.connect_google_ads(
                        api_key=connection_data.get("api_key"),
                        customer_id=connection_data.get("customer_id"),
                        developer_token=connection_data.get("developer_token")
                    )
                elif source_id == "facebook_pixel":
                    success = await self.real_connector_service.connect_facebook_pixel(
                        access_token=connection_data.get("access_token"),
                        pixel_id=connection_data.get("pixel_id")
                    )
                elif source_id == "website":
                    success = await self.real_connector_service.connect_google_analytics(
                        credentials_path=connection_data.get("credentials_path"),
                        property_id=connection_data.get("property_id")
                    )
                else:
                    success = False
                
                if success:
                    self.connections[connection_id] = {
                        "source_id": source_id,
                        "connection_id": connection_id,
                        "status": "connected",
                        "connected_at": datetime.now().isoformat(),
                        "connection_data": connection_data,
                        "real_data": True
                    }
                    return {"connection_id": connection_id, "status": "connected", "real_data": True}
                else:
                    raise Exception("Real data source connection failed")
                    
            except Exception as e:
                print(f"Real data connection failed, falling back to mock: {e}")
                # Fall back to mock data
                pass
        
        # Mock connection (fallback or when real data is disabled)
        await asyncio.sleep(0.5)  # Simulate API call delay
        
        self.connections[connection_id] = {
            "source_id": source_id,
            "connection_id": connection_id,
            "status": "connected",
            "connected_at": datetime.now().isoformat(),
            "connection_data": connection_data,
            "real_data": False
        }
        
        return {"connection_id": connection_id, "status": "connected", "real_data": False}
    
    async def get_all_connections(self) -> List[Dict]:
        """Get all active connections"""
        return list(self.connections.values())
    
    async def disconnect_source(self, connection_id: str):
        """Disconnect a data source"""
        if connection_id in self.connections:
            del self.connections[connection_id]
        else:
            raise Exception("Connection not found")
    
    async def get_source_data(self, source_id: str) -> Dict[str, Any]:
        """Get data from a connected source"""
        # Check if source is connected
        connected = any(conn["source_id"] == source_id for conn in self.connections.values())
        
        if not connected:
            raise Exception(f"Source {source_id} is not connected")
        
        # Return mock data for the source
        if source_id in self.mock_data:
            return self.mock_data[source_id]
        else:
            return {"error": "No data available for this source"}
    
    async def get_aggregated_data(self, source_ids: List[str]) -> Dict[str, Any]:
        """Get aggregated data from multiple sources"""
        if self.use_real_data:
            # Try to get real data first
            try:
                real_data = await self.real_connector_service.get_aggregated_real_data(source_ids)
                if real_data.get("real_data"):
                    return real_data
            except Exception as e:
                print(f"Real data aggregation failed, falling back to mock: {e}")
        
        # Fall back to mock data
        aggregated = {
            "total_audience_size": 0,
            "engagement_metrics": {},
            "conversion_data": {},
            "traffic_insights": {},
            "real_data": False
        }
        
        for source_id in source_ids:
            try:
                data = await self.get_source_data(source_id)
                
                if source_id == "google_ads":
                    aggregated["total_audience_size"] += sum(aud["size"] for aud in data.get("audiences", []))
                    aggregated["engagement_metrics"]["google_ads"] = {
                        "avg_ctr": sum(camp["ctr"] for camp in data.get("campaigns", [])) / len(data.get("campaigns", [1]))
                    }
                
                elif source_id == "facebook_pixel":
                    aggregated["conversion_data"]["facebook"] = {
                        "total_events": sum(event["count"] for event in data.get("events", [])),
                        "avg_conversion_rate": sum(event["conversion_rate"] for event in data.get("events", [])) / len(data.get("events", [1]))
                    }
                
                elif source_id == "website":
                    aggregated["traffic_insights"] = data.get("analytics", {})
                    
            except Exception as e:
                print(f"Error getting data from {source_id}: {e}")
        
        return aggregated
