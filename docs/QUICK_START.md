# 🚀 Quick Start Guide

## ✅ **Environment Structure Fixed**
- `.env` files moved to `orchestrate/` folder
- Proper `.gitignore` and `.dockerignore` added
- Environment variables loaded from orchestrate folder

## 🏃‍♂️ **Quick Test (30 seconds)**

### 1. **Test Backend API**
```bash
cd source/main
python3 test_api.py
```

### 2. **Start Backend**
```bash
cd source/main
python3 main.py
# API runs on http://localhost:8000
```

### 3. **Start Frontend**
```bash
cd source/frontend
npm install
npm run dev
# Frontend runs on http://localhost:3000
```

## 🔧 **Environment Setup**

### **Backend Environment** (`orchestrate/main/.env`)
```bash
OPENAI_API_KEY=sk-test-key-replace-with-real-key
DATABASE_URL=sqlite:///./perplexity_chat.db
USE_REAL_DATA_SOURCES=false
```

### **Frontend Environment** (`orchestrate/frontend/.env`)
```bash
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## 🧪 **Test Results**

✅ **Backend API**: All endpoints working  
✅ **WebSocket Chat**: Real-time communication  
✅ **Data Sources**: Mock data connectors  
✅ **Campaign Generation**: AI-powered campaigns  
✅ **Frontend**: TypeScript/Astro with React  
✅ **Docker**: Containerized deployment  

## 📊 **Real Data Sources**

To enable real data sources:
1. Set `USE_REAL_DATA_SOURCES=true` in `orchestrate/main/.env`
2. Add real API keys (Google Ads, Facebook, Analytics)
3. Follow `docs/REAL_DATA_SOURCES.md` for setup

## 🎯 **Interview Ready**

- ✅ Perplexity-like chat interface
- ✅ 3 data source connectors (mock + real)
- ✅ 4 channel execution (Email, SMS, WhatsApp, Push)
- ✅ AI campaign generation
- ✅ Streaming JSON output
- ✅ Modern TypeScript frontend
- ✅ Docker deployment
- ✅ Comprehensive testing

**Ready for demo! 🎉**
