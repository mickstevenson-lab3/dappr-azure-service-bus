import os
import logging
import dapper
from azure.identity import ManagedIdentityCredential
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.core.exceptions import AzureError

# Set up logging
logging.basicConfig(level=logging.INFO)

# Azure Service Bus configuration
SERVICE_BUS_NAMESPACE = os.getenv("SERVICE_BUS_NAMESPACE")
QUEUE_NAME = os.getenv("QUEUE_NAME")

# Initialize the Managed Identity Credential
def get_managed_identity_credentials():
    try:
        logging.info("Fetching managed identity credentials...")
        return ManagedIdentityCredential()
    except AzureError as e:
        logging.error(f"Error fetching managed identity credentials: {e}")
        raise

# Initialize the ServiceBusClient with Managed Identity authentication
def create_service_bus_client():
    credential = get_managed_identity_credentials()
    client = ServiceBusClient(SERVICE_BUS_NAMESPACE, credential=credential)
    return client

# Push a message to Azure Service Bus
def send_message(message_body):
    try:
        client = create_service_bus_client()
        with client:
            sender = client.get_queue_sender(queue_name=QUEUE_NAME)
            with sender:
                message = ServiceBusMessage(message_body)
                sender.send_messages(message)
                logging.info(f"Sent message: {message_body}")
    except AzureError as e:
        logging.error(f"Error sending message: {e}")

# Retrieve a message from Azure Service Bus
def receive_message():
    try:
        client = create_service_bus_client()
        with client:
            receiver = client.get_queue_receiver(queue_name=QUEUE_NAME)
            with receiver:
                messages = receiver.receive_messages(max_message_count=1, max_wait_time=5)
                for msg in messages:
                    logging.info(f"Received message: {msg}")
                    receiver.complete_message(msg)
    except AzureError as e:
        logging.error(f"Error receiving message: {e}")

# Example function for Dapper integration (this is hypothetical since Dapper typically uses a different architecture)
def send_dapper_message(message_body):
    # Just a placeholder for any dapper logic you want to implement
    logging.info(f"Sending message via Dapper: {message_body}")
    # Use Dapper to send message, etc.

# Kubernetes entry point for the application
if __name__ == "__main__":
    # Example: Send and Receive messages
    send_message("Hello from Azure Service Bus!")
    receive_message()

    # Optionally, send messages via Dapper too
    send_dapper_message("Message sent through Dapper!")
