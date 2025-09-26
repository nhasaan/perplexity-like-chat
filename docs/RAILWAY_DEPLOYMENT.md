# 🚀 Railway Deployment Guide

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **OpenAI API Key**: Get your API key from [OpenAI](https://platform.openai.com/api-keys)

## 🚀 Quick Deployment

### 1. Connect to Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will automatically detect the configuration

### 2. Environment Variables

Set these environment variables in Railway dashboard:

#### Required Variables
```
OPENAI_API_KEY=sk-your-actual-openai-api-key
DATABASE_URL=sqlite:///./perplexity_chat.db
USE_REAL_DATA_SOURCES=false
```

#### Optional Variables
```
DEBUG=false
LOG_LEVEL=INFO
AI_MODEL=gpt-3.5-turbo
AI_MAX_TOKENS=2000
AI_TEMPERATURE=0.7
```

### 3. Deploy

Railway will automatically:
- Build the Docker container
- Deploy your application
- Provide a public URL

## 🔧 Configuration Files

The project includes these Railway-specific files:

- `railway.json` - Railway deployment configuration
- `Procfile` - Process definition for Railway
- `orchestrate/main/Dockerfile` - Production-ready Docker container

## 📊 Monitoring

Railway provides:
- **Logs**: Real-time application logs
- **Metrics**: CPU, memory, and network usage
- **Health Checks**: Automatic health monitoring
- **Scaling**: Automatic scaling based on traffic

## 🔄 Updates

To update your deployment:
1. Push changes to your GitHub repository
2. Railway automatically redeploys
3. Zero-downtime deployments

## 🛠️ Troubleshooting

### Common Issues

1. **Build Failures**
   - Check Dockerfile syntax
   - Verify all dependencies in requirements.txt
   - Check Railway logs for specific errors

2. **Environment Variables**
   - Ensure all required variables are set
   - Check variable names match exactly
   - Verify API keys are valid

3. **Health Check Failures**
   - Verify `/health` endpoint is accessible
   - Check application startup logs
   - Ensure port configuration is correct

### Debug Commands

```bash
# Check application logs
railway logs

# Connect to running container
railway shell

# Check environment variables
railway variables
```

## 🌐 Custom Domain

1. Go to Railway dashboard
2. Select your project
3. Go to "Settings" → "Domains"
4. Add your custom domain
5. Configure DNS records as instructed

## 📈 Scaling

Railway automatically scales your application, but you can configure:

- **Resource Limits**: CPU and memory limits
- **Scaling Policies**: Based on metrics
- **Multiple Instances**: For high availability

## 🔒 Security

- Environment variables are encrypted
- HTTPS is enabled by default
- Database connections are secure
- No sensitive data in logs

## 📞 Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Community Support: [Railway Discord](https://discord.gg/railway)
- Status Page: [status.railway.app](https://status.railway.app)

---

**Ready to deploy! 🎉**

Your Perplexity Chat application will be live at your Railway URL within minutes.
