import requests
from datetime import datetime

SOFASCORE_BASE = "https://api.sofascore.com/api/v1"


def get_scheduled_matches(date_str=None):
    if not date_str:
        date_str = datetime.utcnow().strftime("%Y-%m-%d")

    url = f"{SOFASCORE_BASE}/sport/football/scheduled-events/{date_str}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        events = data.get("events", [])
        matches = []

        for event in events:
            home_team = event.get("homeTeam", {}).get("name")
            away_team = event.get("awayTeam", {}).get("name")
            tournament = event.get("tournament", {}).get("name", "")
            unique_tournament = event.get("tournament", {}).get("uniqueTournament", {}).get("name", "")
            start_timestamp = event.get("startTimestamp")

            if not home_team or not away_team:
                continue

            matches.append({
                "home_team": home_team,
                "away_team": away_team,
                "tournament": tournament or unique_tournament,
                "start_timestamp": start_timestamp,
                "event_id": event.get("id")
            })

        return matches

    except requests.RequestException:
        return []
    except Exception:
        return []
