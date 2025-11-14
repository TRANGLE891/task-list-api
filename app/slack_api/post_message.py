import os
import requests
token = os.environ.get("SLACK_BOT_TOKEN")



url = os.environ.get("SLACK_API_URL")

def post_message_with_slack_bot(text: str) -> dict:
    headers = {
		"Authorization": f"Bearer {token}",
		"Content-Type": "application/json",
	}
    payload = {"channel": "C09Q6QRAJN6", "text": text}

    resp = requests.post(url, headers=headers, json=payload, timeout=10)

    data = resp.json()
    return data