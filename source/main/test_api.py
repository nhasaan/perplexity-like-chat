#!/usr/bin/env python3
"""
Simple test script for the Perexity Chat API
Run this after starting the server to test basic functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.json()}")
    return response.status_code == 200

def test_data_sources():
    """Test data sources endpoints"""
    print("\nTesting data sources...")
    
    # Get available sources
    response = requests.get(f"{BASE_URL}/api/data-sources/")
    print(f"Available sources: {response.json()}")
    
    # Connect to Google Ads
    response = requests.post(
        f"{BASE_URL}/api/data-sources/connect/google_ads",
        json={"api_key": "test_key", "account_id": "test_account"}
    )
    print(f"Google Ads connection: {response.json()}")
    
    # Get connections
    response = requests.get(f"{BASE_URL}/api/data-sources/connections")
    print(f"Active connections: {response.json()}")
    
    return True

def test_campaign_generation():
    """Test campaign generation"""
    print("\nTesting campaign generation...")
    
    campaign_request = {
        "message": "Create a retargeting campaign for cart abandoners with high engagement",
        "data_sources": ["google_ads", "facebook_pixel"],
        "channels": ["email", "sms"],
        "client_id": "test_user"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/campaigns/generate",
        json=campaign_request
    )
    
    result = response.json()
    print(f"Campaign generated: {result.get('success', False)}")
    
    if result.get('success'):
        campaign = result.get('campaign', {})
        print(f"Campaign ID: {campaign.get('campaign_id')}")
        print(f"Campaign Name: {campaign.get('name')}")
        print(f"Channels: {[ch.get('type') for ch in campaign.get('channels', [])]}")
        
        # Test campaign execution
        campaign_id = campaign.get('campaign_id')
        if campaign_id:
            execution_request = {
                "schedule_time": "2024-01-15T10:00:00Z",
                "email_recipients": 1000,
                "sms_recipients": 500
            }
            
            exec_response = requests.post(
                f"{BASE_URL}/api/campaigns/execute/{campaign_id}",
                json=execution_request
            )
            
            exec_result = exec_response.json()
            print(f"Campaign execution: {exec_result.get('success', False)}")
            if exec_result.get('success'):
                print(f"Execution ID: {exec_result.get('execution_id')}")
    
    return result.get('success', False)

def test_chat_interface():
    """Test chat interface"""
    print("\nTesting chat interface...")
    
    chat_request = {
        "message": "Help me create a campaign for high-value customers",
        "client_id": "test_user",
        "timestamp": "2024-01-15T10:00:00Z"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/chat/message",
        json=chat_request
    )
    
    result = response.json()
    print(f"Chat response: {result.get('success', False)}")
    if result.get('success'):
        print(f"AI Response: {result.get('response', '')[:100]}...")
    
    return result.get('success', False)

def main():
    """Run all tests"""
    print("🚀 Testing Perexity Chat API")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Data Sources", test_data_sources),
        ("Campaign Generation", test_campaign_generation),
        ("Chat Interface", test_chat_interface)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"✅ {test_name}: {'PASSED' if result else 'FAILED'}")
        except Exception as e:
            print(f"❌ {test_name}: FAILED - {str(e)}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the server logs for details.")

if __name__ == "__main__":
    main()
