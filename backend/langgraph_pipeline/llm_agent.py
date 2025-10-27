"""LLM Agent - Gemini 2.0 Flash integration with LangChain"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from typing import Dict, Any, List
from config import settings
import logging

logger = logging.getLogger(__name__)

class LLMAgent:
    """LLM Agent using Google Gemini 2.0 Flash"""
    
    def __init__(self):
        self.model_name = settings.GEMINI_MODEL
        self.temperature = settings.TEMPERATURE
        self.max_tokens = settings.MAX_TOKENS
        
        # Initialize Gemini model
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=self.temperature,
            max_output_tokens=self.max_tokens,
            convert_system_message_to_human=True
        )
        
        # Conversation memory
        self.sessions = {}
        
        logger.info(f"✅ LLM Agent initialized with {self.model_name}")
    
    def get_session_memory(self, session_id: str) -> ConversationBufferMemory:
        """Get or create session memory"""
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationBufferMemory(
                return_messages=True,
                memory_key="chat_history"
            )
        return self.sessions[session_id]
    
    async def generate_response(
        self,
        query: str,
        session_id: str,
        tools_available: List[str] = None,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generate AI response using Gemini
        
        Args:
            query: User query
            session_id: Session identifier
            tools_available: List of available MCP tools
            context: Additional context
            
        Returns:
            Dictionary with AI response and metadata
        """
        try:
            memory = self.get_session_memory(session_id)
            
            # Build system prompt
            system_prompt = self._build_system_prompt(tools_available)
            
            # Get chat history
            chat_history = memory.chat_memory.messages
            
            # Build messages
            messages = [
                SystemMessage(content=system_prompt),
                *chat_history,
                HumanMessage(content=query)
            ]
            
            # Add context if provided
            if context:
                context_msg = f"\n\nContext: {context}"
                messages[-1].content += context_msg
            
            # Generate response
            logger.info(f"🤖 Generating response for session {session_id}")
            response = await self.llm.ainvoke(messages)
            
            # Save to memory
            memory.chat_memory.add_user_message(query)
            memory.chat_memory.add_ai_message(response.content)
            
            return {
                "success": True,
                "response": response.content,
                "model": self.model_name,
                "session_id": session_id,
                "tokens_used": response.response_metadata.get("token_usage", {})
            }
            
        except Exception as e:
            logger.error(f"❌ LLM generation error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "session_id": session_id
            }
    
    def _build_system_prompt(self, tools_available: List[str] = None) -> str:
        """Build system prompt with tool information"""
        base_prompt = """You are an advanced AI assistant powered by Google Gemini 2.0 Flash, integrated with multiple MCP (Model Context Protocol) tools.

You can help users with a wide range of tasks by orchestrating various tools and capabilities.

Your capabilities include:
- Natural conversation and question answering
- Web searching and information retrieval
- File management and operations
- Database queries and management
- Email composition and sending
- Google Drive integration
- Workflow automation
- Memory and context management
- Data analytics and insights
- Knowledge base search (RAG)
- External API integration

Guidelines:
1. Be helpful, accurate, and concise
2. When a task requires a tool, clearly indicate which tool you would use
3. Provide step-by-step explanations for complex tasks
4. Ask for clarification when needed
5. Respect user privacy and data security
6. If you're unsure, say so rather than guessing
"""
        
        if tools_available:
            tools_list = "\n".join([f"- {tool}" for tool in tools_available])
            base_prompt += f"\n\nCurrently active MCP tools:\n{tools_list}"
        
        return base_prompt
    
    async def analyze_intent(self, query: str) -> Dict[str, Any]:
        """
        Analyze user intent and suggest appropriate tools
        
        Args:
            query: User query
            
        Returns:
            Dictionary with intent analysis
        """
        try:
            analysis_prompt = f"""Analyze the following user query and determine:
1. The primary intent
2. Which MCP tools would be most helpful (from: web_search, file_manager, database, email, drive, automation, memory, analytics, knowledgebase, api_integration)
3. Any parameters needed

Query: {query}

Respond in a structured format."""

            messages = [
                SystemMessage(content="You are an intent analysis assistant."),
                HumanMessage(content=analysis_prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            
            return {
                "success": True,
                "analysis": response.content,
                "query": query
            }
            
        except Exception as e:
            logger.error(f"❌ Intent analysis error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def clear_session(self, session_id: str):
        """Clear session memory"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"🗑️ Cleared session {session_id}")
    
    def get_session_history(self, session_id: str) -> List[Dict[str, str]]:
        """Get session chat history"""
        if session_id not in self.sessions:
            return []
        
        memory = self.sessions[session_id]
        messages = memory.chat_memory.messages
        
        history = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                history.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                history.append({"role": "assistant", "content": msg.content})
        
        return history
