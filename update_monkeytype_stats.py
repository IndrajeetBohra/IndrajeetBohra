import requests
import re
from pathlib import Path

# 🔧 Replace with your Monkeytype username
USERNAME = "indrajeetbohra"

API_URL = f"https://api.monkeytype.com/users/{USERNAME}"

def fetch_stats():
    try:
        r = requests.get(API_URL, timeout=10)
        r.raise_for_status()
        data = r.json()
        # Extract some key stats
        wpm = data["data"]["personalBests"]["time"]["15"]["wpm"]  # Example: 15s test WPM
        acc = data["data"]["personalBests"]["time"]["15"]["acc"]
        consistency = data["data"]["personalBests"]["time"]["15"]["consistency"]
        return wpm, acc, consistency
    except Exception as e:
        print("Error fetching stats:", e)
        return None, None, None

def update_readme(wpm, acc, consistency):
    readme_path = Path("README.md")
    text = readme_path.read_text()

    new_stats = f"""
![WPM](https://img.shields.io/badge/WPM-{wpm}-blue?style=for-the-badge)
![Accuracy](https://img.shields.io/badge/Accuracy-{acc}%25-green?style=for-the-badge)
![Consistency](https://img.shields.io/badge/Consistency-{consistency}%25-yellow?style=for-the-badge)
    """.strip()

    updated = re.sub(
        r"<!-- MONKEYTYPE-STATS:START -->(.*?)<!-- MONKEYTYPE-STATS:END -->",
        f"<!-- MONKEYTYPE-STATS:START -->\n{new_stats}\n<!-- MONKEYTYPE-STATS:END -->",
        text,
        flags=re.DOTALL,
    )

    readme_path.write_text(updated)

if __name__ == "__main__":
    wpm, acc, consistency = fetch_stats()
    if wpm:
        update_readme(wpm, acc, consistency)
    else:
        print("No stats updated.")
