from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    user_request: str
    goal: str
    plan: str

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview"
)


# Node 1: Understand the request
def analyze_request(state: State) -> State:
    prompt_template = PromptTemplate.from_template(
    "Analyze the user's request and understand the goal.\nUser request: {user_request}")

    chain = prompt_template | llm

    response = chain.invoke({"user_request": state['user_request']})
    
    return {
        "goal": response.content
    }


# Node 2: Generate an Action Plan
def create_plan(state: State) -> State:
    plan_prompt_template = PromptTemplate.from_template(
    "Based on the understanding below, create a clear step-by-step goal:\n{goal}"
    )
    chain = plan_prompt_template | llm
    response = chain.invoke({"goal": state['goal']})
    
    return {
        "plan": response.content
    }



# Build graph
graph = StateGraph(State)
graph.add_node("analyze", analyze_request)
graph.add_node("plan", create_plan)

graph.add_edge(START, "analyze")
graph.add_edge("analyze", "plan")
graph.add_edge("plan", END)

workflow = graph.compile()

result = workflow.invoke({
    "user_request": "Help me plan my workday so I can finish tasks and still have time to relax."
})


Plan = result["plan"]
print("PLAN: ", Plan[0]["text"])


