import json
import glob
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))

def load_snapshot(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def get_two_latest_snapshots():
    pattern = os.path.join(APP_DIR, "figma_snap_shot_*.json")
    files = glob.glob(pattern)
    files.sort(key=os.path.getmtime)
    if len(files) < 2:
        raise ValueError("Need at least 2 snapshots to compare. Run figma.py again.")
    return files[-2], files[-1]

def extract_text_nodes(node, path=""):
    results = {}
    current_path = f"{path}/{node.get('name', '')}"

    if node.get("type") == "TEXT":
        results[node["id"]] = {
            "name": node.get("name"),
            "text": node.get("characters", ""),
            "path": current_path
        }

    for child in node.get("children", []):
        results.update(extract_text_nodes(child, current_path))

    return results

def compare_snapshots(old_nodes, new_nodes):
    changes = {"added": [], "removed": [], "modified": []}

    old_ids = set(old_nodes.keys())
    new_ids = set(new_nodes.keys())

    for node_id in new_ids - old_ids:
        changes["added"].append(new_nodes[node_id])

    for node_id in old_ids - new_ids:
        changes["removed"].append(old_nodes[node_id])

    for node_id in old_ids & new_ids:
        if old_nodes[node_id]["text"] != new_nodes[node_id]["text"]:
            changes["modified"].append({
                "path": new_nodes[node_id]["path"],
                "name": new_nodes[node_id]["name"],
                "old_text": old_nodes[node_id]["text"],
                "new_text": new_nodes[node_id]["text"]
            })

    return changes

def get_latest_changes():
    old_file, new_file = get_two_latest_snapshots()
    print(f"Comparing:\n  OLD: {os.path.basename(old_file)}\n  NEW: {os.path.basename(new_file)}\n")
    old_data = load_snapshot(old_file)
    new_data = load_snapshot(new_file)
    old_nodes = extract_text_nodes(old_data["document"])
    new_nodes = extract_text_nodes(new_data["document"])
    return compare_snapshots(old_nodes, new_nodes)

if __name__ == "__main__":
    changes = get_latest_changes()
    print(json.dumps(changes, indent=2))