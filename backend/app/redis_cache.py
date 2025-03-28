import redis
import json
import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

load_dotenv()  # Load .env file from mounted volume

r = redis.Redis(host="redis", port=6379, decode_responses=True)

def cache_get(key):
    val = r.get(key)
    return json.loads(val) if val else None

def cache_set(key, value, ex=120):
    r.set(key, json.dumps(value), ex=ex)

def load_private_key(file_path=None):
    if file_path is None:
        file_path = os.getenv("PRIVATE_KEY_PATH")
    if not file_path:
        raise ValueError("PRIVATE_KEY_PATH is not set in the environment variables.")

    with open(file_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key
