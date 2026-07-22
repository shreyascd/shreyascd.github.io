#!/usr/bin/env python3
"""Fetch GitHub contributions - uses data-level directly"""
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def fetch_contributions(username: str) -> dict:
    """Fetch contribution data from GitHub."""
    url = f"https://github.com/users/{username}/contributions"
    print(f"📡 Fetching: {url}")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, "html.parser")
    day_cells = soup.find_all("td", {"data-level": True})
    
    if not day_cells:
        print("❌ No cells found")
        return mock_contributions()
    
    print(f"✅ Found {len(day_cells)} cells")
    
    contributions = []
    total_contributions = 0
    max_level = 0
    
    for cell in day_cells:
        level = int(cell.get("data-level", 0))
        date_str = cell.get("data-date", "")
        count = level * 5
        
        contributions.append({"level": level, "count": count, "date": date_str})
        total_contributions += count
        max_level = max(max_level, level)
    
    current_streak = 0
    for cell in reversed(day_cells):
        level = int(cell.get("data-level", 0))
        if level > 0:
            current_streak += 1
        else:
            break
    
    print(f"Last 10 days:")
    for c in contributions[-10:]:
        print(f"  {c['date']}: level={c['level']}")
    
    return {
        "username": username,
        "timestamp": datetime.now().isoformat(),
        "total": total_contributions,
        "max_day": max_level * 5,
        "current_streak": current_streak,
        "grid": contributions,
    }

def mock_contributions() -> dict:
    import random
    grid = []
    for _ in range(53 * 7):
        level = random.randint(0, 5)
        grid.append({"level": level, "count": level * 5})
    return {
        "username": "your-username",
        "timestamp": datetime.now().isoformat(),
        "total": 100,
        "max_day": 25,
        "current_streak": 5,
        "grid": grid,
    }

if __name__ == "__main__":
    username = os.environ.get("GITHUB_ACTOR", "shreyascd")
    try:
        data = fetch_contributions(username)
    except Exception as e:
        print(f"❌ Error: {e}")
        data = mock_contributions()
    
    os.makedirs("../data", exist_ok=True)
    with open("../data/contributions.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved")
