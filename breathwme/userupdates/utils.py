import requests

EXPO_PUSH_ENDPOINT = "https://exp.host/--/api/v2/push/send"

def send_push_notifications(tokens, title, body):
    print(f"send_push_notifications called with tokens: {tokens}, title: {title}, body: {body}")

    messages = [{
        "to": token,
        "sound": "default",
        "title": title,
        "body": body,
        "priority": "high",
    } for token in tokens]

    # ✅ DO NOT wrap in {"messages": messages}
    response = requests.post(EXPO_PUSH_ENDPOINT, json=messages)

    if response.status_code == 200:
        print("Push notifications sent:", response.json())
        return True
    else:
        print("Failed to send push notifications:", response.text)
        return False
