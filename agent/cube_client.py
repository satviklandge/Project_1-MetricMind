import os
import requests
from dotenv import load_dotenv

load_dotenv()

CUBE_URL = os.getenv("CUBE_API_URL")
TOKEN = os.getenv("CUBE_API_TOKEN")


def run_query(query):
    headers = {
        "Authorization": TOKEN
    }

    response = requests.post(
        CUBE_URL,
        headers=headers,
        json=query
    )

    return response.json()