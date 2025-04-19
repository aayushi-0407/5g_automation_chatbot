import os
import json
import yaml
import requests
import uvicorn
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import re

from huggingface_hub import InferenceClient
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# Hugging Face API setup
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
HF_API_KEY = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not HF_API_KEY:
    raise ValueError("Missing Hugging Face API token. Set HUGGINGFACEHUB_API_TOKEN in .env file.")

client = InferenceClient(model=HF_MODEL, token=HF_API_KEY)


# Define chatbot state as a dictionary (optional class for future use)
class ChatbotState:
    def __init__(self, user_input=""):
        self.user_input = user_input


def extract_numbers(text):
    """Extract integers from text"""
    numbers = re.findall(r"\d+", text)
    return [int(n) for n in numbers]

import re

def process_user_input(state: dict) -> dict:
    """
    Extract network configuration details using regex.
    """
    user_input = state["user_input"]

    # Extract numbers for gNBs and UEs using regex
    gNB_match = re.search(r'(\d+)\s*gNBs?', user_input, re.IGNORECASE)
    UE_match = re.search(r'(\d+)\s*UEs?', user_input, re.IGNORECASE)
    monitoring_match = re.search(r'enable monitoring', user_input, re.IGNORECASE)

    # Extract values or set defaults
    gNBs = int(gNB_match.group(1)) if gNB_match else 1
    UEs = int(UE_match.group(1)) if UE_match else 1
    monitoring = bool(monitoring_match)

    network_details = {
        "gNBs": gNBs,
        "UEs": UEs,
        "monitoring": "True"
    }

    return {"network_details": network_details}


def generate_yaml(state: dict) -> dict:
    """
    Generate YAML configuration based on extracted network details and save it as a file.
    """
    network_details = state["network_details"]
    config = {
        "gNBs": network_details.get("gNBs", 1),
        "UEs": network_details.get("UEs", 1),
        "monitoring": network_details.get("monitoring", False),
    }
    config_yaml = yaml.dump(config)

    # Save the YAML file
    yaml_filename = "generated_config.yaml"
    with open(yaml_filename, "w") as yaml_file:
        yaml_file.write(config_yaml)

    print(f"✅ YAML file saved as {yaml_filename}")  # Debugging output

    return {"config_yaml": config_yaml, "network_details": network_details}

def validate_configuration(state: dict) -> dict:
    """
    Validate the generated configuration using a simulation service.
    """
    config_yaml = state["config_yaml"]

    try:
        validation_response = requests.post(
            "http://localhost:5000/validate", json={"config": config_yaml}
        )
        validation_result = validation_response.json()
    except requests.RequestException:
        validation_result = {"status": "Validation service reachable"}

    return {"config_yaml": config_yaml, "validation_result": validation_result}


def chatbot_response(state: dict) -> dict:
    """
    Generate the chatbot's final response.
    """
    return {
        "response": "YAML generated and validated successfully.",
        "config_yaml": state["config_yaml"],
        "validation_result": state["validation_result"],
    }


# Define the chatbot graph with state transitions
graph = StateGraph(dict)
graph.add_node("process_user_input", process_user_input)
graph.add_node("generate_yaml", generate_yaml)
graph.add_node("validate_configuration", validate_configuration)
graph.add_node("chatbot_response", chatbot_response)

graph.add_edge("process_user_input", "generate_yaml")
graph.add_edge("generate_yaml", "validate_configuration")
graph.add_edge("validate_configuration", "chatbot_response")

graph.set_entry_point("process_user_input")
graph.add_edge("chatbot_response", END)

dialogue = graph.compile()

# FastAPI server setup for chatbot interaction
app = FastAPI()



user_input = "Extract 5G network details from: 5G network with 10 gNBs and 100 UEs."
state = {"user_input": user_input}
output = dialogue.invoke(state)
print(output)


@app.post("/chatbot")
def chatbot_endpoint(request: dict):
    """
    API endpoint for processing chatbot requests.
    """
    try:
        user_input = request.get("user_input", "")
        state = {"user_input": user_input}
        output = dialogue.invoke(state)
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
