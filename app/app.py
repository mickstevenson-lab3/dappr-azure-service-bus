import os
import json
import requests
from azure.identity import DefaultAzureCredential
from flask import Flask, request

app = Flask(__name__)

DAPR_PUBSUB_NAME = "servicebus-pubsub"
QUEUE_NAME = "dappr-test"
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")

credential = DefaultAzureCredential()
token = credential.get_token("https://servicebus.azure.net/.default").token

@app.route("/publish", methods=["POST"])
def publish_message():
    data = request.json
    dapr_url = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/{DAPR_PUBSUB_NAME}/{QUEUE_NAME}"
    
    response = requests.post(dapr_url, json=data)
    
    if response.status_code == 204:
        return {"status": "Message published successfully"}
    else:
        return {"error": response.text}, response.status_code

@app.route("/subscribe", methods=["POST"])
def subscribe_message():
    data = request.json
    print("Received message:", json.dumps(data, indent=2))
    return "", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
