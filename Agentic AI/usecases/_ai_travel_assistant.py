from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
# from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# 1. Define Tools (Dummy Logic for Demo)
@tool
def flight_search(destination: str):
    """Search available flights to a destination city."""
    return f"Flights to {destination}: $500"

@tool
def hotel_search(destination: str):
    """Find hotels and accommodation options in a destination city."""
    return f"Hotels in {destination}: $150/night"

@tool
def weather_check(destination: str):
    """Check the current weather conditions for a destination city."""
    return f"Weather in {destination}: Sunny"

tools = [flight_search, hotel_search, weather_check]
tool_node = ToolNode(tools)


# Bind tools to model so it knows when to call them
# model = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)
model = ChatGroq(model="llama-3.1-8b-instruct").bind_tools(tools)
# model = ChatGroq(model="Llama-3.1-8B-Instruct").bind_tools(tools)


# build-in MessagesState Structure
# class MessagesState(TypedDict):
#     messages: Annotated[list[BaseMessage], add_messages]


# 2. Define LLM Call Node
def llm_node(state: MessagesState):
    response = model.invoke(state["messages"])
    return {"messages": [response]}

# 3. Build Graph
builder = StateGraph(MessagesState)
# Add Nodes
builder.add_node("llm_node", llm_node)
builder.add_node("tools", tool_node)
# Add Edges
builder.add_edge(START, "llm_node")
builder.add_conditional_edges("llm_node", tools_condition)
builder.add_edge("tools", "llm_node") # Loop back
builder.add_edge("llm_node", END)
# 4. Compile & Run
workflow = builder.compile()

inputs = {"messages": [("user", "Plan a 3-day trip to Dubai next weekend.")]}
result = workflow.invoke(inputs)
print(result["messages"][-1].content)












































































































