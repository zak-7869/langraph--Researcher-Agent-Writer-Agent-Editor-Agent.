import os
from typing import TypedDict
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

# ==========================================
# 1. DEFINE THE SHARED STATE SCHEMA
# ==========================================
class TeamState(TypedDict):
    """The shared blueprint holding the memory of our multi-agent team."""
    topic: str             # The initial user prompt or assignment
    research_notes: str    # Filled out exclusively by the Researcher Agent
    initial_draft: str     # Filled out exclusively by the Writer Agent
    final_polish: str      # Completed and optimized by the Editor Agent


load_dotenv()
# ==========================================
# 2. INITIALIZE GROQ LLM
# ==========================================
# We use llama-3.3-70b-versatile for high-reasoning orchestration speeds
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3
)

# ==========================================
# 3. DEFINE THE INDEPENDENT AGENT NODES
# ==========================================

def researcher_agent(state: TeamState):
    """Agent 1: Unpacks the topic into structured, factual core concepts."""
    print("\n[Researcher Agent] Analyzing topic and compiling core facts...")
    
    prompt = [
        SystemMessage(content="You are an expert Research Analyst. Your job is to break down the user's topic into a bulleted list of 3-4 factual, core technical insights or historical contexts. Keep it highly detailed but concise."),
        HumanMessage(content=f"Research this topic thoroughly: {state['topic']}")
    ]
    
    response = llm.invoke(prompt)
    # Update state: we only append/update the research_notes key
    return {"research_notes": response.content}


def writer_agent(state: TeamState):
    """Agent 2: Transforms raw research notes into a flowing prose narrative."""
    print("\n[Writer Agent] Transforming research notes into a structured draft...")
    
    prompt = [
        SystemMessage(content="You are an elite Technology and Business Copywriter. Write a compelling, engaging, and beautifully structured 2-paragraph article based exclusively on the provided research notes. Use bold headings."),
        HumanMessage(content=f"Topic: {state['topic']}\n\nResearch Notes Provided:\n{state['research_notes']}")
    ]
    
    response = llm.invoke(prompt)
    # Update state: pass along the draft to the next stage
    return {"initial_draft": response.content}


def editor_agent(state: TeamState):
    """Agent 3: Polishes grammar, structure, tone, and final delivery."""
    print("\n[Editor Agent] Reviewing draft, polishing tone, and applying final edits...")
    
    prompt = [
        SystemMessage(content="You are a Chief Editor. Take the initial draft and critique it for clarity, impact, flow, and structural perfection. Return only the finalized, polished version of the text. Do not add conversational intro/outro text."),
        HumanMessage(content=f"Initial Draft:\n{state['initial_draft']}")
    ]
    
    response = llm.invoke(prompt)
    # Update state: fill out the final step
    return {"final_polish": response.content}

# ==========================================
# 4. ORCHESTRATE THE COMPLEX MULTI-AGENT GRAPH
# ==========================================
workflow = StateGraph(TeamState)

# Step A: Register the independent agents as functional nodes
workflow.add_node("researcher", researcher_agent)
workflow.add_node("writer", writer_agent)
workflow.add_node("editor", editor_agent)

# Step B: Establish the linear pipeline sequence rules
workflow.add_edge(START, "researcher")      # User triggers Researcher first
workflow.add_edge("researcher", "writer")    # Researcher hands off to Writer
workflow.add_edge("writer", "editor")        # Writer hands off to Editor
workflow.add_edge("editor", END)             # Editor marks compilation complete

# Step C: Compile into an active agent application
app = workflow.compile()

# ==========================================
# 5. EXECUTE THE MULTI-AGENT COLLABORATION
# ==========================================
if __name__ == "__main__":
    # Define our starting task
    initial_input = {
        "topic": "The emergence of Agentic AI workflows versus traditional Retrieval-Augmented Generation (RAG)"
    }
    
    print("🤖 STARTING COLLABORATIVE PIPELINE WORKFLOW 🤖")
    
    # Stream the states to see exactly when each agent speaks
    for output in app.stream(initial_input):
        for node_name, state_delta in output.items():
            print(f"--- Finished Node: {node_name.upper()} ---")
            
    # Fetch final absolute results from the compiled application state
    final_results = app.invoke(initial_input)
    
    print("\n=======================================================")
    print("🏆 FINAL OUTPUT DELIVERED BY EDITOR AGENT 🏆")
    print("=======================================================")
    print(final_results["final_polish"])
