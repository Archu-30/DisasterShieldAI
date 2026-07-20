from typing import TypedDict
from langgraph.graph import StateGraph, END

from backend.agents.coordinator import CoordinatorAgent
from backend.agents.disaster_detector import DisasterDetector
from backend.agents.preparedness_agent import PreparednessAgent
from backend.agents.emergency_agent import EmergencyAgent
from backend.agents.information_agent import InformationAgent
from backend.agents.resource_agent import ResourceAgent


# -------------------------
# State
# -------------------------

class DisasterState(TypedDict):
    query: str
    disaster: str
    response: str


# -------------------------
# Agents
# -------------------------

router = CoordinatorAgent()
detector = DisasterDetector()
prep = PreparednessAgent()
emergency = EmergencyAgent()
info = InformationAgent()
resource = ResourceAgent()


# -------------------------
# Nodes
# -------------------------

def coordinator_node(state):

    choice = router.decide_agent(state["query"])
    print("Coordinator chose:", choice)

    if "emergency" in choice:
        return "emergency"

    elif "information" in choice:
        return "information"

    elif "resource" in choice:
        return "resource"

    return "preparedness"


def preparedness_node(state):

    return {
        "response": prep.get_response(
            state["disaster"],
            state["query"]
        )
    }


def emergency_node(state):

    return {
        "response": emergency.get_response(
            state["disaster"],
            state["query"]
        )
    }


def information_node(state):

    return {
        "response": info.get_response(
            state["disaster"],
            state["query"]
        )
    }


def resource_node(state):

    return {
        "response": resource.get_resources(
            state["query"]
        )
    }


# -------------------------
# Build Graph
# -------------------------

workflow = StateGraph(DisasterState)

workflow.add_node("preparedness", preparedness_node)
workflow.add_node("emergency", emergency_node)
workflow.add_node("information", information_node)
workflow.add_node("resource", resource_node)

workflow.set_conditional_entry_point(
    coordinator_node,
    {
        "preparedness": "preparedness",
        "emergency": "emergency",
        "information": "information",
        "resource": "resource",
    },
)

workflow.add_edge("preparedness", END)
workflow.add_edge("emergency", END)
workflow.add_edge("information", END)
workflow.add_edge("resource", END)

graph = workflow.compile()


# -------------------------
# Function for App
# -------------------------

def get_response(user_query):
    try:
        detected_disaster = detector.detect_disaster(user_query)

        result = graph.invoke(
            {
                "query": user_query,
                "disaster": detected_disaster,
                "response": ""
            }
        )

        return {
            "disaster": detected_disaster,
            "response": result["response"]
        }
    except Exception as e:
        err_msg = str(e)
        if "Authentication" in err_msg or "api_key" in err_msg or "401" in err_msg or "Groq" in err_msg:
            return {
                "disaster": "Error",
                "response": "⚠️ **Groq API Key Authentication Error**: Your GROQ_API_KEY is invalid or missing.\n\nPlease check your key at [console.groq.com/keys](https://console.groq.com/keys) and update **Streamlit Cloud Settings → Secrets** (or `.env`)."
            }
        return {
            "disaster": "Error",
            "response": f"⚠️ An error occurred while processing your request: {err_msg}"
        }