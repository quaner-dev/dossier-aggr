import os

RABBITMQ_USERNAME: str = os.getenv("RABBITMQ_USERNAME", "guest")
RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD", "guest")
RABBITMQ_IP: str = os.getenv("RABBITMQ_IP", "localhost")
RABBITMQ_PORT: str = os.getenv("RABBITMQ_PORT", "5672")
