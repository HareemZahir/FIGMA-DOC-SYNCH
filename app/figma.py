#download latest Figma JSON
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

FIGMA_TOKEN = os.getenv("FIGMA_TOKEN")
FILE_KEY = "ZZoZFhIbiyi197NFTfWSDg"

from datetime import datetime


# --- Make the request ---
url = f"https://api.figma.com/v1/files/{FILE_KEY}"
headers = {"X-Figma-Token": FIGMA_TOKEN}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()


    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"figma_snap_shot_{timestamp}.json"
    
    with open(filename,"w",encoding= "utf-8") as f:
        json.dump(data,f,indent=2)

    print(f"Saced snapshot to {filename}")
else:
    print(f"Error{response.status_code}: {response.text}")