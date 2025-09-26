from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

# Chat Models
class ChatMessage(BaseModel):
    message: str
    client_id: str
    timestamp: Optional[str] = None

class ChatResponse(BaseModel):
    success: bool
    response: str
    timestamp: str

# Data Source Models
class DataSourceConnection(BaseModel):
    source_id: str
    connection_data: Dict[str, Any]

class DataSourceInfo(BaseModel):
    id: str
    name: str
    description: str
    status: str

class ConnectionResponse(BaseModel):
    success: bool
    source_id: str
    connection_id: str
    status: str

# Campaign Models
class CampaignRequest(BaseModel):
    message: str
    data_sources: List[str]
    channels: List[str]
    client_id: str

class ChannelConfig(BaseModel):
    type: str
    content: str
    timing: str
    personalization: Dict[str, Any]

class TargetAudience(BaseModel):
    demographics: Dict[str, Any]
    interests: List[str]
    behavior: List[str]

class CampaignExecution(BaseModel):
    schedule: str
    budget: float
    metrics: List[str]

class Campaign(BaseModel):
    campaign_id: str
    name: str
    description: str
    target_audience: TargetAudience
    channels: List[ChannelConfig]
    execution: CampaignExecution
    data_sources: List[str]
    client_id: str
    created_at: str
    status: str

class CampaignResponse(BaseModel):
    success: bool
    campaign: Campaign

# Execution Models
class ExecutionRequest(BaseModel):
    schedule_time: Optional[str] = None
    email_recipients: Optional[int] = None
    sms_recipients: Optional[int] = None
    whatsapp_recipients: Optional[int] = None
    push_recipients: Optional[int] = None

class ExecutionResult(BaseModel):
    execution_id: str
    campaign_id: str
    status: str
    channels: List[Dict[str, Any]]
    executed_at: str
