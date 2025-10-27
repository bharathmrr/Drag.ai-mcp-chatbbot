# 🚀 Deployment Guide - AI-MCP Orchestrator

This guide covers deploying the AI-MCP Orchestrator to production.

---

## 📋 Pre-Deployment Checklist

- [ ] Environment variables configured
- [ ] Database connection tested
- [ ] API keys secured
- [ ] CORS settings updated
- [ ] Build process tested
- [ ] Error handling verified
- [ ] Logging configured

---

## 🌐 Deployment Options

### **Option 1: Railway (Recommended for Backend)**

Railway provides easy deployment with automatic HTTPS and environment management.

#### **Backend Deployment**

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Initialize project:**
   ```bash
   cd backend
   railway init
   ```

4. **Set environment variables:**
   ```bash
   railway variables set GEMINI_API_KEY=your_key_here
   railway variables set MONGODB_URL=your_mongodb_url
   railway variables set HOST=0.0.0.0
   railway variables set PORT=8000
   ```

5. **Deploy:**
   ```bash
   railway up
   ```

6. **Get deployment URL:**
   ```bash
   railway domain
   ```

---

### **Option 2: Render**

#### **Backend on Render**

1. **Create `render.yaml`:**
   ```yaml
   services:
     - type: web
       name: ai-mcp-backend
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
       envVars:
         - key: GEMINI_API_KEY
           sync: false
         - key: MONGODB_URL
           sync: false
   ```

2. **Connect GitHub repo** to Render
3. **Set environment variables** in Render dashboard
4. **Deploy**

---

### **Option 3: Vercel (Frontend)**

#### **Frontend Deployment**

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   cd frontend
   vercel
   ```

3. **Set environment variables:**
   ```bash
   vercel env add VITE_API_URL production
   # Enter your backend URL
   ```

4. **Production deployment:**
   ```bash
   vercel --prod
   ```

---

### **Option 4: Docker + Cloud Provider**

#### **Build Docker Images**

```bash
# Build backend
cd backend
docker build -t ai-mcp-backend .

# Build frontend
cd ../frontend
docker build -t ai-mcp-frontend .
```

#### **Deploy to AWS ECS**

1. **Push to ECR:**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com
   
   docker tag ai-mcp-backend:latest your-account.dkr.ecr.us-east-1.amazonaws.com/ai-mcp-backend:latest
   docker push your-account.dkr.ecr.us-east-1.amazonaws.com/ai-mcp-backend:latest
   ```

2. **Create ECS Task Definition**
3. **Create ECS Service**
4. **Configure Load Balancer**

---

### **Option 5: DigitalOcean App Platform**

1. **Connect GitHub repository**
2. **Configure build settings:**
   - **Backend:** Python, `uvicorn main:app --host 0.0.0.0 --port 8080`
   - **Frontend:** Node.js, `npm run build`
3. **Set environment variables**
4. **Deploy**

---

## 🗄️ Database Setup

### **MongoDB Atlas (Recommended)**

1. **Create cluster** at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. **Get connection string**
3. **Whitelist IP addresses** (or use 0.0.0.0/0 for all)
4. **Set environment variable:**
   ```bash
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/ai_mcp_orchestrator
   ```

### **Self-Hosted MongoDB**

```bash
# Docker
docker run -d -p 27017:27017 --name mongodb mongo:7.0

# Or use docker-compose
docker-compose up -d mongodb
```

---

## 🔐 Security Configuration

### **Environment Variables**

**Never commit these to Git!**

```env
# Production .env
GEMINI_API_KEY=your_production_key
MONGODB_URL=mongodb+srv://...
SMTP_PASSWORD=your_smtp_password
SECRET_KEY=your_secret_key_here

# CORS - Update with your domain
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### **CORS Configuration**

Update `backend/config.py`:
```python
CORS_ORIGINS: list = [
    "https://yourdomain.com",
    "https://www.yourdomain.com"
]
```

### **Rate Limiting**

Add to `backend/main.py`:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/chat/send")
@limiter.limit("10/minute")
async def send_message(request: Request, ...):
    ...
```

---

## 📊 Monitoring & Logging

### **Application Monitoring**

1. **Sentry for Error Tracking:**
   ```bash
   pip install sentry-sdk
   ```
   
   ```python
   import sentry_sdk
   
   sentry_sdk.init(
       dsn="your-sentry-dsn",
       traces_sample_rate=1.0
   )
   ```

2. **LogTail for Logging:**
   ```bash
   pip install logtail-python
   ```

### **Health Checks**

Ensure `/health` endpoint is accessible:
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }
```

---

## 🚦 Performance Optimization

### **Backend**

1. **Enable Gzip compression:**
   ```python
   from fastapi.middleware.gzip import GZipMiddleware
   app.add_middleware(GZipMiddleware, minimum_size=1000)
   ```

2. **Add caching:**
   ```python
   from fastapi_cache import FastAPICache
   from fastapi_cache.backends.redis import RedisBackend
   
   @app.on_event("startup")
   async def startup():
       redis = aioredis.from_url("redis://localhost")
       FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
   ```

3. **Use connection pooling** for MongoDB

### **Frontend**

1. **Build for production:**
   ```bash
   npm run build
   ```

2. **Enable compression** in hosting platform

3. **Use CDN** for static assets

---

## 🔄 CI/CD Pipeline

### **GitHub Actions**

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Railway
        run: |
          npm install -g @railway/cli
          railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
  
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Vercel
        run: |
          npm install -g vercel
          vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
```

---

## 🧪 Production Testing

Before going live:

```bash
# Test backend health
curl https://your-backend.com/health

# Test API endpoint
curl -X POST https://your-backend.com/api/chat/send \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello", "active_tools": []}'

# Test frontend
curl https://your-frontend.com
```

---

## 📈 Scaling

### **Horizontal Scaling**

- Use load balancer (AWS ALB, Nginx)
- Deploy multiple backend instances
- Use Redis for session storage

### **Vertical Scaling**

- Increase server resources
- Optimize database queries
- Enable caching

---

## 🔧 Troubleshooting

### **Common Issues**

**CORS Errors:**
- Update `CORS_ORIGINS` in backend config
- Ensure frontend URL is whitelisted

**Database Connection:**
- Check MongoDB connection string
- Verify IP whitelist
- Test connection locally first

**API Key Issues:**
- Verify Gemini API key is valid
- Check rate limits
- Monitor quota usage

---

## 📝 Post-Deployment

1. **Monitor logs** for errors
2. **Set up alerts** for downtime
3. **Configure backups** for database
4. **Document deployment** process
5. **Create rollback plan**

---

## 🆘 Support

If you encounter issues:
- Check application logs
- Review error messages
- Test locally first
- Open GitHub issue

---

**Deployment complete! Your AI-MCP Orchestrator is now live! 🎉**
