import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

load_dotenv()

FIGMA_TOKEN = os.getenv("FIGMA_TOKEN")
FILE_KEY = "ZZoZFhIbiyi197NFTfWSDg"

APP_DIR = os.path.dirname(os.path.abspath(__file__))

def fetch_snapshot():
    url = f"https://api.figma.com/v1/files/{FILE_KEY}"
    headers = {"X-Figma-Token": FIGMA_TOKEN}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"figma_snap_shot_{timestamp}.json"
        filepath = os.path.join(APP_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"Saved snapshot to {filename}")
        return filepath
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


if __name__ == "__main__":
    fetch_snapshot()