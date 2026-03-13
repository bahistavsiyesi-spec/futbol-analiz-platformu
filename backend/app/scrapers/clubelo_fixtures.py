import requests
import csv
import io
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

CLUBELO_FIXTURES_URL = "http://api.clubelo.com/Fixtures"


def get_upcoming_fixtures():
    try:
        response = requests.get(CLUBELO_FIXTURES_URL, timeout=15)
        response.raise_for_status()

        reader = csv.DictReader(io.StringIO(response.text))
        rows = list(reader)

        fixtures = []

        for row in rows:
            home_team = (
                row.get("Home")
                or row.get("HomeTeam")
                or row.get("Club1")
                or row.get("Team1")
                or ""
            ).strip()

            away_team = (
                row.get("Away")
                or row.get("AwayTeam")
                or row.get("Club2")
                or row.get("Team2")
                or ""
            ).strip()

            country = (row.get("Country") or "").strip()
            league = (row.get("League") or "").strip()
            date = (row.get("Date") or "").strip()

            if not home_team or not away_team:
                continue

            fixtures.append({
                "home_team": home_team,
                "away_team": away_team,
                "country": country,
                "league": league,
                "date": date
            })

        return fixtures

    except requests.RequestException as e:
        logger.warning(f"ClubElo fixtures request hatası: {e}")
        return []
    except Exception as e:
        logger.warning(f"ClubElo fixtures parse hatası: {e}")
        return []


def get_today_fixtures():
    today = datetime.now().strftime("%Y-%m-%d")
    fixtures = get_upcoming_fixtures()

    return [
        match for match in fixtures
        if match.get("date") == today
    ]
