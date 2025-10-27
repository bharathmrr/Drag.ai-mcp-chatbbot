# 🤝 Contributing to AI-MCP Orchestrator

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

---

## 🚀 Getting Started

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/Drag.ai-mcp-chatbbot.git
   cd Drag.ai-mcp-chatbbot
   ```
3. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## 📋 Development Setup

Follow the [SETUP_GUIDE.md](SETUP_GUIDE.md) to set up your development environment.

---

## 🎯 How to Contribute

### **1. Adding a New MCP Tool**

To add a new MCP tool:

1. **Create the tool file** in `backend/mcp_tools/`:
   ```python
   # backend/mcp_tools/your_tool_mcp.py
   
   from typing import Dict, Any
   import logging
   
   logger = logging.getLogger(__name__)
   
   class YourTool:
       """MCP tool for [description]"""
       
       def __init__(self):
           self.name = "your_tool"
           self.description = "Description of what your tool does"
           self.enabled = True
       
       async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
           """Execute tool operation"""
           try:
               # Your implementation here
               return {
                   "success": True,
                   "result": "Your result"
               }
           except Exception as e:
               logger.error(f"❌ Error: {str(e)}")
               return {"success": False, "error": str(e)}
       
       def get_schema(self) -> Dict[str, Any]:
           """Return tool schema for LangChain"""
           return {
               "name": self.name,
               "description": self.description,
               "parameters": {
                   "type": "object",
                   "properties": {
                       "action": {
                           "type": "string",
                           "description": "Action to perform"
                       }
                   },
                   "required": ["action"]
               }
           }
   ```

2. **Register the tool** in `backend/mcp_tools/__init__.py`:
   ```python
   from .your_tool_mcp import YourTool
   
   __all__ = [
       # ... existing tools
       "YourTool",
   ]
   ```

3. **Add icon** in `frontend/src/components/MCPCard.jsx`:
   ```javascript
   import { YourIcon } from 'lucide-react'
   
   const iconMap = {
       // ... existing icons
       your_tool: YourIcon,
   }
   ```

4. **Add keywords** in `backend/langgraph_pipeline/router.py`:
   ```python
   self.tool_keywords = {
       # ... existing keywords
       "your_tool": ["keyword1", "keyword2", "keyword3"],
   }
   ```

---

### **2. Improving the UI**

To enhance the frontend:

1. **Components** are in `frontend/src/components/`
2. **Styles** use Tailwind CSS in `frontend/src/styles/`
3. **State management** is in `frontend/src/context/`

Example - Adding a new component:
```jsx
// frontend/src/components/YourComponent.jsx

import { motion } from 'framer-motion'

const YourComponent = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="glass-effect p-4 rounded-xl"
    >
      {/* Your component content */}
    </motion.div>
  )
}

export default YourComponent
```

---

### **3. Adding API Endpoints**

To add new API endpoints:

1. **Create route file** in `backend/routes/`:
   ```python
   # backend/routes/your_routes.py
   
   from fastapi import APIRouter, HTTPException
   
   router = APIRouter()
   
   @router.get("/your-endpoint")
   async def your_endpoint():
       return {"success": True, "data": "Your data"}
   ```

2. **Register router** in `backend/main.py`:
   ```python
   from routes import your_routes
   
   app.include_router(your_routes.router, prefix="/api/your", tags=["Your"])
   ```

---

### **4. Improving LangGraph Pipeline**

To enhance the orchestration:

1. **Add nodes** in `backend/langgraph_pipeline/graph_builder.py`
2. **Modify routing** in `backend/langgraph_pipeline/router.py`
3. **Enhance LLM agent** in `backend/langgraph_pipeline/llm_agent.py`

---

## 🧪 Testing

### **Backend Tests**

```bash
cd backend
pytest tests/
```

### **Frontend Tests**

```bash
cd frontend
npm test
```

### **Manual Testing**

1. Start the application
2. Test your changes in the UI
3. Check browser console for errors
4. Verify API responses in Network tab

---

## 📝 Code Style

### **Python (Backend)**

- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Use async/await for I/O operations
- Log important events

Example:
```python
async def your_function(param: str) -> Dict[str, Any]:
    """
    Brief description of function.
    
    Args:
        param: Description of parameter
        
    Returns:
        Dictionary with result
    """
    logger.info(f"Processing {param}")
    # Your code here
    return {"success": True}
```

### **JavaScript/React (Frontend)**

- Use functional components
- Use hooks for state management
- Follow ESLint rules
- Use Tailwind for styling
- Add PropTypes or TypeScript types

Example:
```jsx
const YourComponent = ({ prop1, prop2 }) => {
  const [state, setState] = useState(null)
  
  useEffect(() => {
    // Side effects here
  }, [])
  
  return (
    <div className="your-classes">
      {/* Your JSX */}
    </div>
  )
}

export default YourComponent
```

---

## 📦 Commit Guidelines

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

Examples:
```bash
git commit -m "feat: add weather MCP tool"
git commit -m "fix: resolve WebSocket connection issue"
git commit -m "docs: update API reference"
```

---

## 🔍 Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG.md**
5. **Create pull request** with clear description

### **PR Template**

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tested locally
- [ ] Added unit tests
- [ ] Updated documentation

## Screenshots (if applicable)
Add screenshots here
```

---

## 🐛 Reporting Bugs

When reporting bugs, include:

1. **Description** of the bug
2. **Steps to reproduce**
3. **Expected behavior**
4. **Actual behavior**
5. **Screenshots** if applicable
6. **Environment** (OS, Python version, Node version)
7. **Error logs**

---

## 💡 Feature Requests

When requesting features:

1. **Describe the feature**
2. **Explain the use case**
3. **Provide examples**
4. **Suggest implementation** (optional)

---

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Framer Motion](https://www.framer.com/motion/)

---

## 🏆 Contributors

Thank you to all contributors who help make this project better!

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## ❓ Questions?

If you have questions:
- Open a GitHub Discussion
- Check existing issues
- Read the documentation

---

**Thank you for contributing! 🎉**
