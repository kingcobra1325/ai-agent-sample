from handlers import restart_service, scale_service, ignore_alert, print_message, create_pull_request

TOOLS = {
    "restart_service": restart_service,
    "scale_service": scale_service,
    "ignore_alert": ignore_alert,
    "print_message": print_message,
    "create_pull_request": create_pull_request,
}

def execute_action(ai_response: dict):
    action = ai_response.get("action")
    parameters = ai_response.get("parameters", {})
    handler = TOOLS.get(action)
    if handler:
        handler(**parameters)
    else:
        print(f"[ERROR] No handler found for action: {action}")