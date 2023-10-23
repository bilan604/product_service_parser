import os
import base64
from dotenv import load_dotenv
load_dotenv()


def is_valid_user(username, password):
    ADMIN_USERNAME = os.getenv("LOGIN_USERNAME").strip()
    ADMIN_PASSWORD = os.getenv("LOGIN_PASSWORD").strip()
    if username.strip() == ADMIN_USERNAME and password.strip() == ADMIN_PASSWORD:
        return True
    return False

def encrypt(input_string):
    encoded_bytes = base64.b64encode(input_string.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def decrypt(encoded_string):
    decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))
    return decoded_bytes.decode('utf-8')


