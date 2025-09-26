# Real Data Source Integration Guide

This guide explains how to connect to actual data sources for production use.

## 🔌 **Real Data Source Setup**

### **1. Google Ads API Integration**

#### Prerequisites:
- Google Ads account with API access
- Google Cloud Console project
- OAuth 2.0 credentials

#### Setup Steps:

1. **Create Google Cloud Project**
   ```bash
   # Go to Google Cloud Console
   # Create new project or select existing
   # Enable Google Ads API
   ```

2. **Get API Credentials**
   ```bash
   # In Google Cloud Console:
   # 1. Go to APIs & Services > Credentials
   # 2. Create OAuth 2.0 Client ID
   # 3. Download credentials JSON
   ```

3. **Configure Environment Variables**
   ```bash
   # Add to .env file
   GOOGLE_ADS_API_KEY=your_api_key
   GOOGLE_ADS_CUSTOMER_ID=123-456-7890
   GOOGLE_ADS_DEVELOPER_TOKEN=your_developer_token
   GOOGLE_ADS_CLIENT_ID=your_client_id
   GOOGLE_ADS_CLIENT_SECRET=your_client_secret
   ```

4. **Test Connection**
   ```python
   from services.real_data_connectors import GoogleAdsConnector
   
   connector = GoogleAdsConnector(
       api_key=os.getenv("GOOGLE_ADS_API_KEY"),
       customer_id=os.getenv("GOOGLE_ADS_CUSTOMER_ID"),
       developer_token=os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN")
   )
   
   audiences = await connector.get_audiences()
   print(f"Found {len(audiences)} audiences")
   ```

### **2. Facebook Pixel API Integration**

#### Prerequisites:
- Facebook Business account
- Facebook Pixel installed on website
- Facebook App with Marketing API access

#### Setup Steps:

1. **Create Facebook App**
   ```bash
   # Go to Facebook Developers
   # Create new app > Business
   # Add Marketing API product
   ```

2. **Get Access Token**
   ```bash
   # In Facebook App Dashboard:
   # 1. Go to Marketing API > Tools
   # 2. Generate access token
   # 3. Select required permissions
   ```

3. **Configure Environment Variables**
   ```bash
   # Add to .env file
   FACEBOOK_ACCESS_TOKEN=your_access_token
   FACEBOOK_PIXEL_ID=your_pixel_id
   FACEBOOK_APP_ID=your_app_id
   FACEBOOK_APP_SECRET=your_app_secret
   ```

4. **Test Connection**
   ```python
   from services.real_data_connectors import FacebookPixelConnector
   
   connector = FacebookPixelConnector(
       access_token=os.getenv("FACEBOOK_ACCESS_TOKEN"),
       pixel_id=os.getenv("FACEBOOK_PIXEL_ID")
   )
   
   events = await connector.get_events("2024-01-01", "2024-01-31")
   print(f"Found {len(events)} events")
   ```

### **3. Google Analytics 4 Integration**

#### Prerequisites:
- Google Analytics 4 property
- Google Cloud Console project
- Service account with Analytics access

#### Setup Steps:

1. **Create Service Account**
   ```bash
   # In Google Cloud Console:
   # 1. Go to IAM & Admin > Service Accounts
   # 2. Create new service account
   # 3. Download JSON key file
   ```

2. **Enable Analytics API**
   ```bash
   # In Google Cloud Console:
   # 1. Go to APIs & Services > Library
   # 2. Search for "Google Analytics Reporting API"
   # 3. Enable the API
   ```

3. **Configure Environment Variables**
   ```bash
   # Add to .env file
   GOOGLE_ANALYTICS_CREDENTIALS_PATH=/path/to/credentials.json
   GOOGLE_ANALYTICS_PROPERTY_ID=123456789
   ```

4. **Test Connection**
   ```python
   from services.real_data_connectors import GoogleAnalyticsConnector
   
   connector = GoogleAnalyticsConnector(
       credentials_path=os.getenv("GOOGLE_ANALYTICS_CREDENTIALS_PATH"),
       property_id=os.getenv("GOOGLE_ANALYTICS_PROPERTY_ID")
   )
   
   data = await connector.get_analytics_data("2024-01-01", "2024-01-31")
   print(f"Analytics data: {data}")
   ```

## 🚀 **Production Deployment**

### **Environment Configuration**

Create a production `.env` file:

```bash
# Production Environment Variables
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://user:pass@host:port/db

# Google Ads
GOOGLE_ADS_API_KEY=your_production_key
GOOGLE_ADS_CUSTOMER_ID=your_customer_id
GOOGLE_ADS_DEVELOPER_TOKEN=your_developer_token

# Facebook Pixel
FACEBOOK_ACCESS_TOKEN=your_production_token
FACEBOOK_PIXEL_ID=your_pixel_id

# Google Analytics
GOOGLE_ANALYTICS_CREDENTIALS_PATH=/app/credentials/analytics.json
GOOGLE_ANALYTICS_PROPERTY_ID=your_property_id

# Security
SECRET_KEY=your_secret_key
JWT_SECRET=your_jwt_secret
```

### **Docker Production Setup**

```dockerfile
# Dockerfile.prod
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY source/main/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY source/main/ .

# Create credentials directory
RUN mkdir -p /app/credentials

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "main.py"]
```

### **Docker Compose for Production**

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  perplexity-chat:
    build:
      context: ..
      dockerfile: orchestrate/main/Dockerfile.prod
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
      - GOOGLE_ADS_API_KEY=${GOOGLE_ADS_API_KEY}
      - FACEBOOK_ACCESS_TOKEN=${FACEBOOK_ACCESS_TOKEN}
      - GOOGLE_ANALYTICS_PROPERTY_ID=${GOOGLE_ANALYTICS_PROPERTY_ID}
    volumes:
      - ./credentials:/app/credentials:ro
    restart: unless-stopped
```

## 🧪 **Testing Real Connections**

### **Test Script for Real Data Sources**

```python
# test_real_connections.py
import asyncio
import os
from dotenv import load_dotenv
from services.real_data_connectors import RealDataConnectorService

async def test_real_connections():
    load_dotenv()
    
    service = RealDataConnectorService()
    
    # Test Google Ads
    print("Testing Google Ads connection...")
    google_ads_connected = await service.connect_google_ads(
        api_key=os.getenv("GOOGLE_ADS_API_KEY"),
        customer_id=os.getenv("GOOGLE_ADS_CUSTOMER_ID"),
        developer_token=os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN")
    )
    print(f"Google Ads: {'✅ Connected' if google_ads_connected else '❌ Failed'}")
    
    # Test Facebook Pixel
    print("Testing Facebook Pixel connection...")
    facebook_connected = await service.connect_facebook_pixel(
        access_token=os.getenv("FACEBOOK_ACCESS_TOKEN"),
        pixel_id=os.getenv("FACEBOOK_PIXEL_ID")
    )
    print(f"Facebook Pixel: {'✅ Connected' if facebook_connected else '❌ Failed'}")
    
    # Test Google Analytics
    print("Testing Google Analytics connection...")
    analytics_connected = await service.connect_google_analytics(
        credentials_path=os.getenv("GOOGLE_ANALYTICS_CREDENTIALS_PATH"),
        property_id=os.getenv("GOOGLE_ANALYTICS_PROPERTY_ID")
    )
    print(f"Google Analytics: {'✅ Connected' if analytics_connected else '❌ Failed'}")
    
    # Get aggregated data
    if any([google_ads_connected, facebook_connected, analytics_connected]):
        print("\nFetching real data...")
        data = await service.get_aggregated_real_data(["google_ads", "facebook_pixel", "website"])
        print(f"Real data fetched: {len(data)} metrics")
        print(f"Total audience size: {data.get('total_audience_size', 0)}")

if __name__ == "__main__":
    asyncio.run(test_real_connections())
```

## 🔒 **Security Considerations**

### **API Key Management**
- Store API keys in environment variables
- Use secrets management in production
- Rotate keys regularly
- Monitor API usage

### **Rate Limiting**
- Implement rate limiting for API calls
- Cache responses when appropriate
- Handle API errors gracefully

### **Data Privacy**
- Ensure GDPR compliance
- Implement data retention policies
- Encrypt sensitive data
- Audit data access

## 📊 **Monitoring and Analytics**

### **Health Checks**
```python
# Add to main.py
@app.get("/health/datasources")
async def health_check_data_sources():
    """Check health of all data source connections"""
    health_status = {}
    
    for source_id, connector in data_connector_service.connectors.items():
        try:
            # Test connection
            await connector.test_connection()
            health_status[source_id] = "healthy"
        except Exception as e:
            health_status[source_id] = f"unhealthy: {str(e)}"
    
    return {"data_sources": health_status}
```

### **Usage Metrics**
- Track API call counts
- Monitor response times
- Alert on failures
- Generate usage reports

This guide provides everything needed to connect to real data sources in production!
