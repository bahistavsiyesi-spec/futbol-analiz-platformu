import requests
import csv
import io
import logging

logger = logging.getLogger(__name__)

CLUBELO_BASE = "http://api.clubelo.com"


def get_team_elo(team_name):
    formatted = team_name.replace(" ", "").replace("-", "")

    try:
        resp = requests.get(f"{CLUBELO_BASE}/{formatted}", timeout=10)
        resp.raise_for_status()

        reader = csv.DictReader(io.StringIO(resp.text))
        rows = list(reader)

        if not rows:
            return None

        latest = rows[-1]

        elo_value = latest.get("Elo", 0)
        try:
            elo_value = round(float(elo_value))
        except (TypeError, ValueError):
            elo_value = 0

        return {
            "team": latest.get("Club", team_name),
            "elo": elo_value,
            "country": latest.get("Country", "")
        }

    except requests.RequestException as e:
        logger.warning(f"ClubElo request hatası: {team_name} - {e}")
        return None
    except Exception as e:
        logger.warning(f"ClubElo veri işleme hatası: {team_name} - {e}")
        return None
