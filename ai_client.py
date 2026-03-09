import requests
from typing import Dict, Any
import json
import os

AI_ENDPOINT = os.getenv("AI_ENDPOINT")
API_KEY = os.getenv("AI_API_KEY")

def call_ai_agent(alert: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send alert and context to AI Agent endpoint and receive structured JSON decision.
    """
    # Prepare the payload for the AI
    payload = {"messages":[{
        "role": "system", "content": f"""
You are an automation AI agent. You receive the following alert and context.

Choose the best action to take from the following allowed actions (parameters are in the parenthesis with its datatype):
- print_message
- restart_service
- scale_service
- ignore_alert
etc. refer to the allowed_actions for more info. It is setup into tuples (action_name, parameters:type)

Return your answer ONLY as JSON in this format:
{{
  "action": "<action_name>",
  "reason": "<message for the reason on taking the action>"
  "parameters": {{}}
}}

If there are no valid actions to take, simply set the action as null and provide the
failure on reason
"""},{"role": "user", "content": f"Alert: {alert}\nContext{context}"}],
        "max_tokens": 500,
        "temperature": 0
    }

    headers = {
        "Content-Type": "application/json",
    }

    # Add API key if using cloud endpoint
    if "openrouter" in AI_ENDPOINT.lower():
        headers["Authorization"] = f"Bearer {API_KEY}"
        ai_endpoint
    else:
        ai_endpoint = f"{AI_ENDPOINT}/chat/completions"

    response = requests.post(ai_endpoint, json=payload, headers=headers)
    response.raise_for_status()
    
    # Parse AI JSON output
    ai_decision = response.json()
    # Assuming AI returns the JSON inside 'text' field (common in LM Studio/OpenRouter)
    print(f"\n{json.dumps(ai_decision, indent=3)}\n")
    return json.loads(ai_decision["choices"][0]["message"]["content"])