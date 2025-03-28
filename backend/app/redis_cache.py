import redis
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

r = redis.Redis(host="redis", port=6379, decode_responses=True)

def cache_get(key):
    val = r.get(key)
    return json.loads(val) if val else None

def cache_set(key, value, ex=120):
    r.set(key, json.dumps(value), ex=ex)

def load_private_key(file_path):
    with open(file_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key
