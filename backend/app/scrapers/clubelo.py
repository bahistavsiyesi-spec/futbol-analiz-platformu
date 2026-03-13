import requests
import csv
import io

CLUBELO_BASE = "http://api.clubelo.com"

def get_team_elo(team_name):
    formatted = team_name.replace(" ", "").replace("-", "")

    resp = requests.get(CLUBELO_BASE + "/" + formatted, timeout=10)

    reader = csv.DictReader(io.StringIO(resp.text))
    rows = list(reader)

    if not rows:
        return None

    latest = rows[-1]

    return {
        "team": latest.get("Club", team_name),
        "elo": round(float(latest.get("Elo", 0))),
        "country": latest.get("Country", "")
    }
