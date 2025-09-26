import openai
import json
from typing import Dict, List, Any
import os
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.chat_histories: Dict[str, List[Dict]] = {}
        
    async def process_chat_message(self, message: str, client_id: str) -> str:
        """Process a chat message and generate AI response"""
        try:
            # Get or create chat history for client
            if client_id not in self.chat_histories:
                self.chat_histories[client_id] = []
            
            # Add user message to history
            self.chat_histories[client_id].append({
                "role": "user",
                "content": message
            })
            
            # Create system prompt for marketing campaign context
            system_prompt = """You are an AI marketing campaign assistant. You help users create targeted marketing campaigns by:
1. Analyzing their data sources (Google Ads, Facebook Pixel, Website analytics)
2. Understanding their target audience and goals
3. Recommending the right channels (Email, SMS, WhatsApp, Push notifications)
4. Generating executable campaign JSON payloads

Always respond in a helpful, conversational manner. When users ask about campaigns, provide specific recommendations based on their data sources and suggest the most effective channels for their goals."""
            
            # Prepare messages for OpenAI
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.chat_histories[client_id][-10:])  # Last 10 messages for context
            
            # Generate response
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Add AI response to history
            self.chat_histories[client_id].append({
                "role": "assistant",
                "content": ai_response
            })
            
            return ai_response
            
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try again."
    
    async def generate_campaign_json(self, context: str, data_sources: List[str], channels: List[str]) -> Dict[str, Any]:
        """Generate a campaign JSON payload based on context and available data"""
        
        campaign_prompt = f"""
        Based on the following context and available data sources, generate a marketing campaign JSON payload:
        
        Context: {context}
        Data Sources: {', '.join(data_sources)}
        Channels: {', '.join(channels)}
        
        Generate a JSON payload with the following structure:
        {{
            "campaign_id": "unique_campaign_id",
            "name": "Campaign Name",
            "description": "Campaign description",
            "target_audience": {{
                "demographics": {{}},
                "interests": [],
                "behavior": []
            }},
            "channels": [
                {{
                    "type": "email|sms|whatsapp|push",
                    "content": "Message content",
                    "timing": "optimal_time",
                    "personalization": {{}}
                }}
            ],
            "execution": {{
                "schedule": "immediate|scheduled",
                "budget": 0,
                "metrics": []
            }}
        }}
        
        Make it realistic and actionable for the given context.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": campaign_prompt}],
                max_tokens=800,
                temperature=0.7
            )
            
            # Try to parse JSON from response
            content = response.choices[0].message.content
            # Extract JSON from the response (in case there's extra text)
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Fallback if JSON parsing fails
                return {
                    "campaign_id": f"campaign_{hash(context)}",
                    "name": "Generated Campaign",
                    "description": content,
                    "target_audience": {"demographics": {}, "interests": [], "behavior": []},
                    "channels": [{"type": "email", "content": "Default message", "timing": "immediate", "personalization": {}}],
                    "execution": {"schedule": "immediate", "budget": 0, "metrics": []}
                }
                
        except Exception as e:
            # Return a default campaign structure if AI fails
            return {
                "campaign_id": f"campaign_{hash(context)}",
                "name": "Default Campaign",
                "description": f"Campaign for: {context}",
                "target_audience": {"demographics": {}, "interests": [], "behavior": []},
                "channels": [{"type": "email", "content": "Default message", "timing": "immediate", "personalization": {}}],
                "execution": {"schedule": "immediate", "budget": 0, "metrics": []}
            }
    
    async def get_chat_history(self, client_id: str) -> List[Dict]:
        """Get chat history for a client"""
        return self.chat_histories.get(client_id, [])
    
    async def clear_chat_history(self, client_id: str):
        """Clear chat history for a client"""
        if client_id in self.chat_histories:
            self.chat_histories[client_id] = []
