import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

CLIENT_NAME = os.getenv("CLIENT_NAME", "account")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
