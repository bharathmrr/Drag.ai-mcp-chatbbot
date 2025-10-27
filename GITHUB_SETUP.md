# 🚀 GitHub Setup & CI/CD Guide

## 📋 Prerequisites

- Git installed on your system
- GitHub account
- Docker Hub account (for container registry)

---

## 🎯 Step 1: Initialize Git Repository

Open terminal in your project directory and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: AI-MCP Orchestrator with real tools and CI/CD"
```

---

## 🌐 Step 2: Create GitHub Repository

### Option A: Using GitHub Website

1. Go to https://github.com/new
2. Repository name: `Drag.ai-mcp-chatbbot`
3. Description: `AI-MCP Orchestrator with Gemini 2.0 Flash and 17 MCP Tools`
4. Choose: **Public** or **Private**
5. **DO NOT** initialize with README (we already have one)
6. Click **Create repository**

### Option B: Using GitHub CLI

```bash
gh repo create Drag.ai-mcp-chatbbot --public --source=. --remote=origin
```

---

## 🔗 Step 3: Connect Local to GitHub

```bash
# Add GitHub remote
git remote add origin https://github.com/bharathmrr/Drag.ai-mcp-chatbbot.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 🔐 Step 4: Set Up GitHub Secrets

For CI/CD to work, you need to add secrets to your GitHub repository:

### Navigate to Repository Settings:
1. Go to your GitHub repository
2. Click **Settings** tab
3. Click **Secrets and variables** → **Actions**
4. Click **New repository secret**

### Add These Secrets:

#### 1. DOCKER_USERNAME
- **Name:** `DOCKER_USERNAME`
- **Value:** Your Docker Hub username (e.g., `bharathmrr`)

#### 2. DOCKER_PASSWORD
- **Name:** `DOCKER_PASSWORD`
- **Value:** Your Docker Hub password or access token
  - Get token: https://hub.docker.com/settings/security
  - Click **New Access Token**
  - Name: `github-actions`
  - Copy the token

#### 3. GEMINI_API_KEY (Optional for deployment)
- **Name:** `GEMINI_API_KEY`
- **Value:** `AIzaSyD-Zay55zScSxixu87JsLZcsCSzLKJRjuo`

---

## 🐳 Step 5: Set Up Docker Hub Repository

1. Go to https://hub.docker.com
2. Click **Create Repository**
3. Name: `ai-mcp-orchestrator`
4. Visibility: **Public**
5. Click **Create**

Your Docker image will be: `bharathmrr/ai-mcp-orchestrator`

---

## ⚙️ Step 6: CI/CD Pipeline Overview

The GitHub Actions workflow (`.github/workflows/ci-cd.yml`) will automatically:

### On Every Push/PR:
- ✅ Test backend (Python)
- ✅ Test frontend (Node.js)
- ✅ Run linting and checks

### On Push to Main Branch:
- ✅ Build Docker image
- ✅ Push to Docker Hub
- ✅ Tag with commit SHA and `latest`
- ✅ Deploy (if configured)

---

## 🔄 Step 7: Trigger First CI/CD Run

```bash
# Make a small change
echo "# AI-MCP Orchestrator" >> GITHUB_SETUP.md

# Commit and push
git add .
git commit -m "docs: Add GitHub setup guide"
git push origin main
```

### View Pipeline:
1. Go to your GitHub repository
2. Click **Actions** tab
3. See your workflow running! 🎉

---

## 📊 Step 8: Monitor CI/CD Pipeline

### Pipeline Jobs:

1. **Test Backend** (2-3 minutes)
   - Install Python dependencies
   - Run tests
   - Check code quality

2. **Test Frontend** (2-3 minutes)
   - Install Node dependencies
   - Build production bundle
   - Run tests

3. **Build and Push** (5-7 minutes)
   - Build Docker image
   - Push to Docker Hub
   - Tag with SHA and latest

4. **Deploy** (1-2 minutes)
   - Deployment notification
   - Ready for production

---

## 🐳 Step 9: Pull and Run Docker Image

Once CI/CD completes, anyone can run your app:

```bash
# Pull the image
docker pull bharathmrr/ai-mcp-orchestrator:latest

# Run the container
docker run -d \
  -p 8000:8000 \
  -p 3000:3000 \
  -e GEMINI_API_KEY=your_api_key_here \
  --name ai-mcp \
  bharathmrr/ai-mcp-orchestrator:latest

# Check logs
docker logs -f ai-mcp

# Access the app
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

---

## 🔧 Step 10: Using Docker Compose

```bash
# Create .env file
echo "GEMINI_API_KEY=AIzaSyD-Zay55zScSxixu87JsLZcsCSzLKJRjuo" > .env

# Start with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 📝 Complete Git Workflow

### Initial Setup (One Time):
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/bharathmrr/Drag.ai-mcp-chatbbot.git
git branch -M main
git push -u origin main
```

### Daily Development:
```bash
# Create feature branch
git checkout -b feature/new-tool

# Make changes
# ... edit files ...

# Commit changes
git add .
git commit -m "feat: Add new MCP tool"

# Push to GitHub
git push origin feature/new-tool

# Create Pull Request on GitHub
# After review, merge to main
# CI/CD will automatically deploy
```

---

## 🎯 Branch Strategy

### Main Branch (`main`)
- Production-ready code
- Protected branch
- Requires PR review
- Auto-deploys on merge

### Develop Branch (`develop`)
- Integration branch
- Feature branches merge here first
- Test before merging to main

### Feature Branches
- `feature/tool-name`
- `fix/bug-description`
- `docs/update-readme`

---

## 🔍 Verify Everything Works

### 1. Check GitHub Repository
```bash
# Visit your repo
https://github.com/bharathmrr/Drag.ai-mcp-chatbbot
```

### 2. Check GitHub Actions
```bash
# Visit actions page
https://github.com/bharathmrr/Drag.ai-mcp-chatbbot/actions
```

### 3. Check Docker Hub
```bash
# Visit Docker Hub
https://hub.docker.com/r/bharathmrr/ai-mcp-orchestrator
```

### 4. Test Docker Image
```bash
docker pull bharathmrr/ai-mcp-orchestrator:latest
docker run -p 8000:8000 -p 3000:3000 bharathmrr/ai-mcp-orchestrator:latest
```

---

## 🚨 Troubleshooting

### Issue: CI/CD Fails on Docker Push

**Solution:** Check Docker Hub credentials
```bash
# Verify secrets in GitHub Settings → Secrets
DOCKER_USERNAME = bharathmrr
DOCKER_PASSWORD = <your-token>
```

### Issue: Build Fails

**Solution:** Check logs in GitHub Actions
1. Go to Actions tab
2. Click on failed workflow
3. Click on failed job
4. Read error messages

### Issue: Docker Image Too Large

**Solution:** Optimize Dockerfile
- Use `.dockerignore`
- Multi-stage builds
- Remove unnecessary files

### Issue: Tests Failing

**Solution:** Run tests locally first
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

---

## 📚 Useful Commands

### Git Commands:
```bash
# Check status
git status

# View commit history
git log --oneline

# Create new branch
git checkout -b branch-name

# Switch branches
git checkout main

# Pull latest changes
git pull origin main

# View remotes
git remote -v

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

### Docker Commands:
```bash
# List images
docker images

# List containers
docker ps -a

# Remove container
docker rm container-name

# Remove image
docker rmi image-name

# View logs
docker logs container-name

# Execute command in container
docker exec -it container-name bash
```

### Docker Compose Commands:
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild and start
docker-compose up -d --build

# View running services
docker-compose ps
```

---

## 🎉 Success Checklist

- [ ] Git repository initialized
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] GitHub secrets configured
- [ ] Docker Hub repository created
- [ ] CI/CD pipeline running
- [ ] Docker image built and pushed
- [ ] Can pull and run Docker image
- [ ] Frontend accessible on port 3000
- [ ] Backend accessible on port 8000
- [ ] MCP tools working
- [ ] AI responses generating

---

## 🔗 Important Links

- **GitHub Repo:** https://github.com/bharathmrr/Drag.ai-mcp-chatbbot
- **GitHub Actions:** https://github.com/bharathmrr/Drag.ai-mcp-chatbbot/actions
- **Docker Hub:** https://hub.docker.com/r/bharathmrr/ai-mcp-orchestrator
- **Documentation:** See README.md

---

## 📞 Quick Reference

### Clone Repository:
```bash
git clone https://github.com/bharathmrr/Drag.ai-mcp-chatbbot.git
cd Drag.ai-mcp-chatbbot
```

### Run with Docker:
```bash
docker-compose up -d
```

### Run Locally:
```bash
# Backend
cd backend
python real_ai_server.py

# Frontend (new terminal)
cd frontend
npm run dev
```

---

## 🎯 Next Steps

1. **Push to GitHub** ✅
2. **Configure Secrets** ✅
3. **Watch CI/CD Run** ✅
4. **Pull Docker Image** ✅
5. **Deploy to Production** 🚀

**Your AI-MCP Orchestrator is now on GitHub with full CI/CD! 🎉**
