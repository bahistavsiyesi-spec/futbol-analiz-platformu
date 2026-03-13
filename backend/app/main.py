from fastapi import FastAPI
from app.scrapers.clubelo import get_team_elo

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Futbol Analiz API çalışıyor"}


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
        "team1": team1_data,
        "team2": team2_data,
        "elo_difference": elo_diff
    }
