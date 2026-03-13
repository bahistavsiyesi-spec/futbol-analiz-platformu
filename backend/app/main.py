from fastapi import FastAPI
from app.scrapers.clubelo import get_team_elo
from app.scrapers.clubelo_fixtures import get_upcoming_fixtures, get_today_fixtures
from app.services.analyzer import analyze_match

app = FastAPI(
    title="Futbol Analiz API",
    description="Takım Elo verilerini çekip maç analizi yapan API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Futbol Analiz API çalışıyor",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/team-elo/{team_name}")
def team_elo(team_name: str):
    data = get_team_elo(team_name)

    if not data:
        return {"error": "Takım bulunamadı"}

    return data


@app.get("/compare-teams/{team1}/{team2}")
def compare_teams(team1: str, team2: str):

    team1_data = get_team_elo(team1)
    team2_data = get_team_elo(team2)

    if not team1_data or not team2_data:
        return {"error": "Takımlardan biri bulunamadı"}

    elo_diff = team1_data["elo"] - team2_data["elo"]

    return {
        "match": f"{team1_data.get('team', team1)} vs {team2_data.get('team', team2)}",
        "team1": team1_data,
        "team2": team2_data,
        "elo_difference": elo_diff
    }


@app.get("/analyze-match/{team1}/{team2}")
def analyze_match_endpoint(team1: str, team2: str):

    team1_data = get_team_elo(team1)
    team2_data = get_team_elo(team2)

    if not team1_data or not team2_data:
        return {"error": "Takımlardan biri bulunamadı"}

    analysis = analyze_match(team1_data, team2_data)

    return {
        "match": f"{team1_data.get('team', team1)} vs {team2_data.get('team', team2)}",
        "team1": team1_data,
        "team2": team2_data,
        "analysis": analysis
    }


@app.get("/today-matches")
def today_matches():

    matches = get_today_fixtures()

    return {
        "count": len(matches),
        "matches": matches
    }


@app.get("/upcoming-matches")
def upcoming_matches():

    matches = get_upcoming_fixtures()

    return {
        "count": len(matches),
        "matches": matches
    }
