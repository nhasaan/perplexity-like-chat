#!/usr/bin/env python3
"""
Comprehensive test script for the Perexity Chat API with real data source testing
Run this after starting the server to test all functionality
"""

import requests
import json
import time
import asyncio
import websockets
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_data_sources():
    """Test data sources endpoints"""
    print("\n🔍 Testing data sources...")
    
    try:
        # Get available sources
        response = requests.get(f"{BASE_URL}/api/data-sources/", timeout=10)
        if response.status_code == 200:
            sources = response.json()
            print(f"✅ Found {len(sources.get('sources', []))} data sources")
            
            # Test connecting to each source
            for source in sources.get('sources', []):
                source_id = source.get('id')
                print(f"  🔗 Testing connection to {source.get('name')}...")
                
                connect_response = requests.post(
                    f"{BASE_URL}/api/data-sources/connect/{source_id}",
                    json={
                        "api_key": f"test_key_{source_id}",
                        "account_id": f"test_account_{source_id}"
                    },
                    timeout=10
                )
                
                if connect_response.status_code == 200:
                    print(f"    ✅ {source.get('name')} connected successfully")
                else:
                    print(f"    ❌ {source.get('name')} connection failed: {connect_response.status_code}")
            
            return True
        else:
            print(f"❌ Failed to get data sources: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Data sources test error: {e}")
        return False

def test_campaign_generation():
    """Test campaign generation with real data flow"""
    print("\n🔍 Testing campaign generation...")
    
    try:
        # First, connect to data sources
        data_sources = ["google_ads", "facebook_pixel", "website"]
        connected_sources = []
        
        for source_id in data_sources:
            connect_response = requests.post(
                f"{BASE_URL}/api/data-sources/connect/{source_id}",
                json={"api_key": f"test_key_{source_id}", "account_id": f"test_account_{source_id}"},
                timeout=10
            )
            if connect_response.status_code == 200:
                connected_sources.append(source_id)
        
        print(f"  📊 Connected to {len(connected_sources)} data sources")
        
        # Generate campaign
        campaign_request = {
            "message": "Create a retargeting campaign for high-value customers who abandoned their cart. Focus on email and SMS channels with personalized messaging.",
            "data_sources": connected_sources,
            "channels": ["email", "sms", "whatsapp", "push"],
            "client_id": "test_user_real"
        }
        
        print("  🤖 Generating campaign...")
        response = requests.post(
            f"{BASE_URL}/api/campaigns/generate",
            json=campaign_request,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                campaign = result.get('campaign', {})
                print(f"  ✅ Campaign generated successfully!")
                print(f"    📋 Campaign ID: {campaign.get('campaign_id')}")
                print(f"    📝 Name: {campaign.get('name')}")
                print(f"    📊 Channels: {[ch.get('type') for ch in campaign.get('channels', [])]}")
                print(f"    🎯 Audience: {campaign.get('target_audience', {}).get('demographics', {})}")
                
                # Test campaign execution
                campaign_id = campaign.get('campaign_id')
                if campaign_id:
                    print("  🚀 Testing campaign execution...")
                    execution_request = {
                        "schedule_time": "2024-01-15T10:00:00Z",
                        "email_recipients": 1000,
                        "sms_recipients": 500,
                        "whatsapp_recipients": 200,
                        "push_recipients": 1500
                    }
                    
                    exec_response = requests.post(
                        f"{BASE_URL}/api/campaigns/execute/{campaign_id}",
                        json=execution_request,
                        timeout=15
                    )
                    
                    if exec_response.status_code == 200:
                        exec_result = exec_response.json()
                        print(f"    ✅ Campaign executed successfully!")
                        print(f"    🆔 Execution ID: {exec_result.get('execution_id')}")
                        print(f"    📊 Status: {exec_result.get('status')}")
                        return True
                    else:
                        print(f"    ❌ Campaign execution failed: {exec_response.status_code}")
                        return False
                else:
                    print("    ❌ No campaign ID returned")
                    return False
            else:
                print(f"  ❌ Campaign generation failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Campaign generation request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Campaign generation test error: {e}")
        return False

async def test_websocket_chat():
    """Test WebSocket chat functionality"""
    print("\n🔍 Testing WebSocket chat...")
    
    try:
        client_id = f"test_client_{int(time.time())}"
        uri = f"{WS_URL}/ws/{client_id}"
        
        async with websockets.connect(uri) as websocket:
            print(f"  🔗 Connected to WebSocket: {client_id}")
            
            # Send test message
            test_message = {
                "type": "chat_message",
                "message": "Hello! Can you help me create a marketing campaign for new customers?",
                "timestamp": "2024-01-15T10:00:00Z"
            }
            
            await websocket.send(json.dumps(test_message))
            print("  📤 Sent test message")
            
            # Wait for response
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                data = json.loads(response)
                
                if data.get('type') == 'ai_response':
                    print("  ✅ Received AI response")
                    print(f"    🤖 Response: {data.get('content', '')[:100]}...")
                    return True
                else:
                    print(f"  ❌ Unexpected response type: {data.get('type')}")
                    return False
                    
            except asyncio.TimeoutError:
                print("  ❌ WebSocket response timeout")
                return False
                
    except Exception as e:
        print(f"❌ WebSocket test error: {e}")
        return False

def test_chat_api():
    """Test REST API chat functionality"""
    print("\n🔍 Testing REST API chat...")
    
    try:
        chat_request = {
            "message": "I need help creating a campaign for cart abandoners with high engagement rates",
            "client_id": "test_user_api",
            "timestamp": "2024-01-15T10:00:00Z"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/chat/message",
            json=chat_request,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("  ✅ Chat API response received")
                print(f"    🤖 AI Response: {result.get('response', '')[:100]}...")
                return True
            else:
                print(f"  ❌ Chat API failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Chat API request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Chat API test error: {e}")
        return False

def test_campaign_history():
    """Test campaign history functionality"""
    print("\n🔍 Testing campaign history...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/campaigns/history/test_user_real", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            campaigns = result.get('campaigns', [])
            print(f"  ✅ Found {len(campaigns)} campaigns in history")
            
            for i, campaign in enumerate(campaigns[:3]):  # Show first 3
                print(f"    📋 Campaign {i+1}: {campaign.get('name', 'Unnamed')}")
                print(f"      🆔 ID: {campaign.get('campaign_id', 'N/A')}")
                print(f"      📊 Channels: {[ch.get('type') for ch in campaign.get('channels', [])]}")
            
            return True
        else:
            print(f"❌ Campaign history request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Campaign history test error: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Testing Perexity Chat API - Comprehensive Test Suite")
    print("=" * 70)
    
    tests = [
        ("Health Check", test_health),
        ("Data Sources", test_data_sources),
        ("Campaign Generation", test_campaign_generation),
        ("REST API Chat", test_chat_api),
        ("Campaign History", test_campaign_history),
        ("WebSocket Chat", test_websocket_chat)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
            print(f"✅ {test_name}: {'PASSED' if result else 'FAILED'}")
        except Exception as e:
            print(f"❌ {test_name}: FAILED - {str(e)}")
            results.append((test_name, False))
        
        print()  # Add spacing between tests
    
    print("=" * 70)
    print("📊 Test Results Summary:")
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The API is working perfectly.")
        print("\n📋 Next Steps:")
        print("  1. Set up real data source credentials (see docs/REAL_DATA_SOURCES.md)")
        print("  2. Configure OpenAI API key in .env file")
        print("  3. Start the frontend: cd source/frontend && npm run dev")
        print("  4. Open http://localhost:3000 to test the UI")
    else:
        print("⚠️  Some tests failed. Check the server logs for details.")
        print("\n🔧 Troubleshooting:")
        print("  1. Make sure the server is running: python main.py")
        print("  2. Check if all dependencies are installed: pip install -r requirements.txt")
        print("  3. Verify OpenAI API key is set in .env file")

if __name__ == "__main__":
    asyncio.run(main())
