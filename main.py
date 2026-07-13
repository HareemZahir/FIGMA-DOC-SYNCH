import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))

import figma
import compare
import llm

def run_pipeline():
    print("Step 1: Fetching latest Figma snapshot...")
    figma.fetch_snapshot()

    print("\nStep 2: Comparing with previous snapshot...")
    changes = compare.get_latest_changes()

    if not changes["added"] and not changes["removed"] and not changes["modified"]:
        print("\nNo changes detected.")
        return

    print("\nStep 3: Summarizing changes with Gemini...")
    summary = llm.summarize_changes(changes)

    print("\n=== Change Summary ===")
    print(summary)

if __name__ == "__main__":
    run_pipeline()