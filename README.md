# Perplexity Chat - AI Marketing Campaign Platform

A complete Perplexity-like chat interface for AI-powered marketing campaign orchestration, built with FastAPI, TypeScript/Astro frontend, and real data source integrations.

## 🎯 **Project Overview**

This platform allows marketers to:
- **Chat with AI** to create targeted marketing campaigns
- **Connect to real data sources** (Google Ads, Facebook Pixel, Website Analytics)
- **Generate executable campaigns** across multiple channels (Email, SMS, WhatsApp, Push)
- **Execute campaigns** with real-time monitoring

## 🏗️ **Architecture**

```
perplexity-chat/
├── source/
│   ├── main/                    # FastAPI Backend
│   │   ├── api/                 # REST API endpoints
│   │   ├── services/            # Business logic
│   │   ├── models/              # Data models
│   │   └── main.py              # Application entry point
│   └── frontend/                # Astro + TypeScript Frontend
│       ├── src/
│       │   ├── pages/           # Astro pages
│       │   ├── components/      # React components
│       │   └── layouts/          # Layout templates
│       └── package.json          # Frontend dependencies
├── orchestrate/                 # Docker deployment
│   ├── compose.yml              # Docker Compose
│   └── main/Dockerfile          # Backend container
└── docs/                        # Documentation
    ├── requirements.txt         # Project requirements
    └── REAL_DATA_SOURCES.md     # Real data integration guide
```

## 🚀 **Quick Start**

📖 **See the complete setup guide**: [`docs/QUICK_START.md`](docs/QUICK_START.md)

### **Quick Commands**

```bash
# Backend
cd source/main && python main.py

# Frontend  
cd source/frontend && npm run dev

# Docker
cd orchestrate && docker-compose up --build
```

### **Environment Setup**

```bash
# Copy environment template
cp orchestrate/main/.env.example orchestrate/main/.env
# Edit .env with your OpenAI API key
```

## 🔌 **Real Data Source Integration**

### **Mock Data (Default)**
The system works out-of-the-box with realistic mock data for demonstration.

### **Real Data Sources**
To connect to actual APIs, follow the guide in `docs/REAL_DATA_SOURCES.md`:

1. **Google Ads API**
   - Set up Google Cloud project
   - Enable Google Ads API
   - Configure OAuth credentials

2. **Facebook Pixel API**
   - Create Facebook Business account
   - Set up Facebook App
   - Generate access tokens

3. **Google Analytics 4**
   - Create service account
   - Enable Analytics API
   - Configure credentials

### **Enable Real Data**
```bash
# Add to orchestrate/main/.env file
USE_REAL_DATA_SOURCES=true
GOOGLE_ADS_API_KEY=your_key
FACEBOOK_ACCESS_TOKEN=your_token
GOOGLE_ANALYTICS_PROPERTY_ID=your_id
```

## 🎨 **Frontend Features**

- **Perplexity-like Chat Interface**: Real-time WebSocket communication
- **Data Source Management**: Connect/disconnect data sources
- **Campaign Visualization**: View generated campaigns
- **Responsive Design**: Modern UI with Tailwind CSS
- **TypeScript**: Full type safety

## 🔧 **API Endpoints**

### **Chat Interface**
- `POST /api/chat/message` - Send chat message
- `WebSocket /ws/{client_id}` - Real-time chat
- `GET /api/chat/history/{client_id}` - Chat history

### **Data Sources**
- `GET /api/data-sources/` - List available sources
- `POST /api/data-sources/connect/{source_id}` - Connect source
- `GET /api/data-sources/connections` - Active connections
- `DELETE /api/data-sources/disconnect/{connection_id}` - Disconnect

### **Campaigns**
- `POST /api/campaigns/generate` - Generate campaign
- `POST /api/campaigns/execute/{campaign_id}` - Execute campaign
- `GET /api/campaigns/history/{client_id}` - Campaign history

## 📊 **Data Sources**

1. **Google Ads Tag** - Audience insights and campaign data
2. **Facebook Pixel** - Behavioral data and retargeting
3. **Website Analytics** - General analytics and user behavior

## 📱 **Channels**

1. **Email** - Direct email marketing campaigns
2. **SMS** - Mobile SMS marketing campaigns
3. **WhatsApp** - WhatsApp messaging campaigns
4. **Push Notifications** - Mobile app push notifications

## 🐳 **Docker Deployment**

```bash
# Build and run with Docker Compose
cd orchestrate
docker-compose up --build
```

## 🧪 **Testing**

### **Basic API Test**
```bash
cd source/main
python test_api.py
```

### **Comprehensive Test**
```bash
cd source/main
python test_real_api.py
```

### **Frontend Test**
```bash
cd source/frontend
npm run test
```

## 📈 **Example Usage**

### **1. Connect Data Sources**
```bash
curl -X POST "http://localhost:8000/api/data-sources/connect/google_ads" \
  -H "Content-Type: application/json" \
  -d '{"api_key": "your_key", "customer_id": "123-456-7890"}'
```

### **2. Generate Campaign**
```bash
curl -X POST "http://localhost:8000/api/campaigns/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a campaign for cart abandoners",
    "data_sources": ["google_ads", "facebook_pixel"],
    "channels": ["email", "sms"],
    "client_id": "user123"
  }'
```

### **3. Execute Campaign**
```bash
curl -X POST "http://localhost:8000/api/campaigns/execute/{campaign_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "schedule_time": "2024-01-15T10:00:00Z",
    "email_recipients": 1000,
    "sms_recipients": 500
  }'
```

## 🔒 **Security & Production**

- **Environment Variables**: Secure API key management
- **CORS Configuration**: Configured for development
- **Rate Limiting**: Built-in API rate limiting
- **Error Handling**: Comprehensive error management
- **Logging**: Structured logging for monitoring

## 📚 **Documentation**

- [`docs/QUICK_START.md`](docs/QUICK_START.md) - Complete setup guide
- [`docs/REAL_DATA_SOURCES.md`](docs/REAL_DATA_SOURCES.md) - Real data source integration
- [`docs/RAILWAY_DEPLOYMENT.md`](docs/RAILWAY_DEPLOYMENT.md) - Railway deployment guide
- `source/main/README.md` - Backend documentation
- `source/frontend/README.md` - Frontend documentation

## 🎯 **Interview Ready Features**

✅ **Perplexity-like Chat Interface** - Real-time WebSocket chat  
✅ **3 Data Source Connectors** - Google Ads, Facebook Pixel, Website  
✅ **4 Channel Execution** - Email, SMS, WhatsApp, Push  
✅ **AI Campaign Generation** - OpenAI-powered campaign creation  
✅ **Streaming JSON Output** - Executable campaign payloads  
✅ **Real Data Integration** - Production-ready API connectors  
✅ **Modern Frontend** - TypeScript/Astro with React components  
✅ **Docker Deployment** - Containerized application  
✅ **Comprehensive Testing** - Full test suite  
✅ **Documentation** - Complete setup and usage guides  

## 🚀 **Next Steps**

1. **Set up real data sources** following `docs/REAL_DATA_SOURCES.md`
2. **Configure OpenAI API key** in `.env` file
3. **Deploy to production** using Docker
4. **Monitor and scale** based on usage

This platform is ready for interview demonstration and can be extended for production use!
