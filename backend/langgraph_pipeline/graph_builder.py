"""Graph Builder - Build LangGraph orchestration pipeline"""

from langgraph.graph import StateGraph, END
from typing import Dict, Any, TypedDict, Annotated
from typing_extensions import TypedDict
import operator
from .llm_agent import LLMAgent
from .router import ToolRouter
import logging

logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    """State for the agent graph"""
    query: str
    session_id: str
    active_tools: list
    messages: Annotated[list, operator.add]
    tool_results: dict
    final_response: str
    error: str

class GraphBuilder:
    """Build and manage LangGraph orchestration pipeline"""
    
    def __init__(self, tool_registry):
        self.tool_registry = tool_registry
        self.llm_agent = LLMAgent()
        self.router = ToolRouter(tool_registry)
        self.graph = self._build_graph()
        
        logger.info("✅ LangGraph pipeline built")
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("analyze_intent", self._analyze_intent_node)
        workflow.add_node("route_tools", self._route_tools_node)
        workflow.add_node("execute_tools", self._execute_tools_node)
        workflow.add_node("generate_response", self._generate_response_node)
        
        # Add edges
        workflow.set_entry_point("analyze_intent")
        workflow.add_edge("analyze_intent", "route_tools")
        workflow.add_conditional_edges(
            "route_tools",
            self._should_use_tools,
            {
                "use_tools": "execute_tools",
                "direct_response": "generate_response"
            }
        )
        workflow.add_edge("execute_tools", "generate_response")
        workflow.add_edge("generate_response", END)
        
        return workflow.compile()
    
    async def _analyze_intent_node(self, state: AgentState) -> AgentState:
        """Analyze user intent"""
        try:
            logger.info("📊 Analyzing intent...")
            
            analysis = await self.llm_agent.analyze_intent(state["query"])
            
            state["messages"].append({
                "node": "analyze_intent",
                "result": analysis
            })
            
            return state
            
        except Exception as e:
            logger.error(f"❌ Intent analysis error: {str(e)}")
            state["error"] = str(e)
            return state
    
    async def _route_tools_node(self, state: AgentState) -> AgentState:
        """Route to appropriate tools"""
        try:
            logger.info("🔀 Routing to tools...")
            
            routing = await self.router.route_query(
                state["query"],
                state.get("active_tools", [])
            )
            
            state["messages"].append({
                "node": "route_tools",
                "result": routing
            })
            
            return state
            
        except Exception as e:
            logger.error(f"❌ Routing error: {str(e)}")
            state["error"] = str(e)
            return state
    
    async def _execute_tools_node(self, state: AgentState) -> AgentState:
        """Execute selected tools"""
        try:
            logger.info("🔧 Executing tools...")
            
            # Get routing info from messages
            routing_msg = next(
                (m for m in state["messages"] if m.get("node") == "route_tools"),
                None
            )
            
            if not routing_msg:
                return state
            
            routing = routing_msg["result"]
            matched_tools = routing.get("matched_tools", [])
            
            if not matched_tools:
                return state
            
            # Execute primary tool (simplified - in production, execute based on query)
            primary_tool = matched_tools[0]["tool"]
            
            # Mock execution - in production, parse query to extract action and params
            result = await self.router.execute_tool(
                primary_tool,
                "execute",
                {}
            )
            
            state["tool_results"] = {primary_tool: result}
            state["messages"].append({
                "node": "execute_tools",
                "result": result
            })
            
            return state
            
        except Exception as e:
            logger.error(f"❌ Tool execution error: {str(e)}")
            state["error"] = str(e)
            return state
    
    async def _generate_response_node(self, state: AgentState) -> AgentState:
        """Generate final response"""
        try:
            logger.info("💬 Generating response...")
            
            # Build context from tool results
            context = {
                "tool_results": state.get("tool_results", {}),
                "active_tools": state.get("active_tools", [])
            }
            
            # Generate response
            response = await self.llm_agent.generate_response(
                state["query"],
                state["session_id"],
                state.get("active_tools", []),
                context
            )
            
            state["final_response"] = response.get("response", "")
            state["messages"].append({
                "node": "generate_response",
                "result": response
            })
            
            return state
            
        except Exception as e:
            logger.error(f"❌ Response generation error: {str(e)}")
            state["error"] = str(e)
            state["final_response"] = f"Error: {str(e)}"
            return state
    
    def _should_use_tools(self, state: AgentState) -> str:
        """Decide whether to use tools or generate direct response"""
        routing_msg = next(
            (m for m in state["messages"] if m.get("node") == "route_tools"),
            None
        )
        
        if not routing_msg:
            return "direct_response"
        
        routing = routing_msg["result"]
        matched_tools = routing.get("matched_tools", [])
        
        # Use tools if we have matches
        if matched_tools and len(matched_tools) > 0:
            return "use_tools"
        
        return "direct_response"
    
    async def run(
        self,
        query: str,
        session_id: str,
        active_tools: list = None
    ) -> Dict[str, Any]:
        """
        Run the graph with a query
        
        Args:
            query: User query
            session_id: Session identifier
            active_tools: List of active tool names
            
        Returns:
            Final state with response
        """
        try:
            # Initialize state
            initial_state = AgentState(
                query=query,
                session_id=session_id,
                active_tools=active_tools or [],
                messages=[],
                tool_results={},
                final_response="",
                error=""
            )
            
            # Run graph
            final_state = await self.graph.ainvoke(initial_state)
            
            return {
                "success": not final_state.get("error"),
                "response": final_state.get("final_response", ""),
                "tool_results": final_state.get("tool_results", {}),
                "error": final_state.get("error"),
                "session_id": session_id
            }
            
        except Exception as e:
            logger.error(f"❌ Graph execution error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "session_id": session_id
            }
