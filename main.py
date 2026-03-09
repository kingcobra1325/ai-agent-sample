from dotenv import load_dotenv

load_dotenv()

from ai_client import call_ai_agent
from router import execute_action
import json

print("=== AI Agent System Control Demo ===")
print("Type system events or alerts. Type 'exit' to quit.\n")

# Define the system context once
system_context = {
    "services": ["worker", "payment-api", "api"],
    "allowed_actions": [
        ("restart_service", {"service": "str"}),
        ("scale_service", {"service": "str", "replicas": "int"}),
        ("ignore_alert", {"alert_id": str}),
        ("print_message", {"message": "str"}),
        ("create_pull_request", {
            "repo": "str",
            "owner": "str",
            "branch": "str",
            "title": "str",
            "base": "str",
            "body": "str",
            }),
        ],
    "system_state": {
        "worker": {"status": "running", "replicas": 2, "memory_usage": "60%"},
        "payment-api": {"status": "running", "replicas": 1, "error_rate": "5%"},
        "api": {"status": "running", "replicas": 1}
    }
}

while True:
    user_input = input("\n[USER INPUT] Describe the system event: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting AI Agent Demo.")
        break

    # Wrap user input as an 'alert'
    alert = {
        "type": "user_event",
        "description": user_input
    }

    try:
        # Send alert + context to AI Agent
        ai_response = call_ai_agent(alert, system_context)
        print(f"[AI DECISION] {json.dumps(ai_response, indent=2)}")

        # Execute the decision
        execute_action(ai_response)
    except Exception as e:
        print(f"[ERROR] Failed to process input: {e}")