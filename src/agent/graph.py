from langchain.messages import AnyMessage, SystemMessage, ToolMessage
from langgraph.graph.state import RunnableConfig
from langgraph.graph import StateGraph, START, END 

from typing_extensions import TypedDict, Annotated 
import operator 

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add] 
    llm_calls: int