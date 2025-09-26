from typing import Dict, List, Any
import json
import uuid
from datetime import datetime
from services.ai_service import AIService
from services.data_connector_service import DataConnectorService

class CampaignService:
    def __init__(self):
        self.ai_service = AIService()
        self.data_service = DataConnectorService()
        self.campaigns: Dict[str, Dict] = {}
        self.executions: Dict[str, Dict] = {}
    
    async def generate_campaign(self, message: str, data_sources: List[str], channels: List[str], client_id: str) -> Dict[str, Any]:
        """Generate a campaign based on context and data sources"""
        try:
            # Get aggregated data from connected sources
            aggregated_data = await self.data_service.get_aggregated_data(data_sources)
            
            # Create context for AI
            context = f"""
            User Request: {message}
            Available Data Sources: {', '.join(data_sources)}
            Selected Channels: {', '.join(channels)}
            Aggregated Data: {json.dumps(aggregated_data, indent=2)}
            """
            
            # Generate campaign using AI
            campaign_json = await self.ai_service.generate_campaign_json(
                context, data_sources, channels
            )
            
            # Add metadata
            campaign_id = str(uuid.uuid4())
            campaign_json["campaign_id"] = campaign_id
            campaign_json["client_id"] = client_id
            campaign_json["data_sources"] = data_sources
            campaign_json["channels"] = channels
            campaign_json["created_at"] = datetime.now().isoformat()
            campaign_json["status"] = "generated"
            
            # Store campaign
            self.campaigns[campaign_id] = campaign_json
            
            return campaign_json
            
        except Exception as e:
            # Return a default campaign if generation fails
            campaign_id = str(uuid.uuid4())
            default_campaign = {
                "campaign_id": campaign_id,
                "name": "Default Campaign",
                "description": f"Campaign for: {message}",
                "client_id": client_id,
                "data_sources": data_sources,
                "channels": channels,
                "target_audience": {"demographics": {}, "interests": [], "behavior": []},
                "channels": [{"type": channel, "content": f"Message for {channel}", "timing": "immediate", "personalization": {}} for channel in channels],
                "execution": {"schedule": "immediate", "budget": 0, "metrics": []},
                "created_at": datetime.now().isoformat(),
                "status": "generated"
            }
            self.campaigns[campaign_id] = default_campaign
            return default_campaign
    
    async def execute_campaign(self, campaign_id: str, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a generated campaign"""
        if campaign_id not in self.campaigns:
            raise Exception("Campaign not found")
        
        campaign = self.campaigns[campaign_id]
        execution_id = str(uuid.uuid4())
        
        # Simulate campaign execution for each channel
        execution_results = []
        
        for channel_config in campaign.get("channels", []):
            channel_type = channel_config.get("type", "email")
            
            # Simulate channel execution
            result = await self._execute_channel(campaign_id, channel_type, channel_config, execution_data)
            execution_results.append(result)
        
        # Store execution
        execution_record = {
            "execution_id": execution_id,
            "campaign_id": campaign_id,
            "status": "executed",
            "channels": execution_results,
            "executed_at": datetime.now().isoformat(),
            "execution_data": execution_data
        }
        
        self.executions[execution_id] = execution_record
        
        return execution_record
    
    async def _execute_channel(self, campaign_id: str, channel_type: str, channel_config: Dict, execution_data: Dict) -> Dict[str, Any]:
        """Execute campaign for a specific channel"""
        import asyncio
        await asyncio.sleep(0.1)  # Simulate execution time
        
        # Channel-specific execution logic
        if channel_type == "email":
            return {
                "channel": "email",
                "status": "sent",
                "recipients": execution_data.get("email_recipients", 1000),
                "message": channel_config.get("content", "Default email message"),
                "scheduled_for": execution_data.get("schedule_time", "immediate")
            }
        
        elif channel_type == "sms":
            return {
                "channel": "sms",
                "status": "sent",
                "recipients": execution_data.get("sms_recipients", 500),
                "message": channel_config.get("content", "Default SMS message"),
                "scheduled_for": execution_data.get("schedule_time", "immediate")
            }
        
        elif channel_type == "whatsapp":
            return {
                "channel": "whatsapp",
                "status": "sent",
                "recipients": execution_data.get("whatsapp_recipients", 200),
                "message": channel_config.get("content", "Default WhatsApp message"),
                "scheduled_for": execution_data.get("schedule_time", "immediate")
            }
        
        elif channel_type == "push":
            return {
                "channel": "push",
                "status": "sent",
                "recipients": execution_data.get("push_recipients", 1500),
                "message": channel_config.get("content", "Default push message"),
                "scheduled_for": execution_data.get("schedule_time", "immediate")
            }
        
        else:
            return {
                "channel": channel_type,
                "status": "failed",
                "error": f"Unsupported channel: {channel_type}"
            }
    
    async def get_campaign_history(self, client_id: str) -> List[Dict]:
        """Get campaign history for a client"""
        client_campaigns = [
            campaign for campaign in self.campaigns.values() 
            if campaign.get("client_id") == client_id
        ]
        return sorted(client_campaigns, key=lambda x: x.get("created_at", ""), reverse=True)
