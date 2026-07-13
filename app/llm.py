import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"

def summarize_changes(changes):
    """
    Takes the changes dict from compare.py and asks Gemini
    to write a plain-English summary.
    """
    prompt = f"""You are a documentation assistant for a fintech mobile app.
Below is a list of changes detected in the app's Figma design file.
Write a short, clear summary of what changed, in plain English,
suitable for a user manual changelog.

Changes (JSON):
{json.dumps(changes, indent=2)}

Write the summary as a few short bullet points."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={GEMINI_API_KEY}"

    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(url, json=body)

    if response.status_code == 200:
        data = response.json()
        summary_text = data["candidates"][0]["content"]["parts"][0]["text"]
        return summary_text
    else:
        return f"Error {response.status_code}: {response.text}"


if __name__ == "__main__":
    # Quick manual test using a fake changes dict for now
    test_changes = {
        "added": [],
        "removed": [],
        "modified": [
            {
                "path": "/Document/Page 1/umme rubab",
                "name": "umme rubab",
                "old_text": "Hareem",
                "new_text": "umme rubab"
            }
        ]
    }

    summary = summarize_changes(test_changes)
    print(summary)
