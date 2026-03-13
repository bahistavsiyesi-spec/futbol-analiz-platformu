from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.scrapers.clubelo import get_team_elo
from app.scrapers.clubelo_fixtures import get_upcoming_fixtures, get_today_fixtures
from app.services.analyzer import analyze_match

app = FastAPI(
    title="Futbol Analiz API",
    description="Takım Elo verilerini çekip maç analizi yapan API",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


class AnalyzeMatchRequest(BaseModel):
    home_team: str
    away_team: str


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/team-elo/{team_name}")
def team_elo(team_name: str):
    data = get_team_elo(team_name)

    if not data:
        raise HTTPException(status_code=404, detail="Takım bulunamadı")

    return data


@app.get("/compare-teams/{team1}/{team2}")
def compare_teams(team1: str, team2: str):
    team1_data = get_team_elo(team1)
    team2_data = get_team_elo(team2)

    if not team1_data or not team2_data:
        raise HTTPException(status_code=404, detail="Takımlardan biri bulunamadı")

    elo_diff = team1_data["elo"] - team2_data["elo"]

    return {
        "match": f"{team1_data.get('team', team1)} vs {team2_data.get('team', team2)}",
        "team1": team1_data,
        "team2": team2_data,
        "elo_difference": elo_diff
    }


@app.get("/analyze-match/{team1}/{team2}")
def analyze_match_get(team1: str, team2: str):
    team1_data = get_team_elo(team1)
    team2_data = get_team_elo(team2)

    if not team1_data or not team2_data:
        raise HTTPException(status_code=404, detail="Takımlardan biri bulunamadı")

    analysis = analyze_match(team1_data, team2_data)

    return {
        "match": f"{team1_data.get('team', team1)} vs {team2_data.get('team', team2)}",
        "team1": team1_data,
        "team2": team2_data,
        "analysis": analysis
    }


@app.post("/analyze-match")
def analyze_match_post(payload: AnalyzeMatchRequest):
    home_team = payload.home_team.strip()
    away_team = payload.away_team.strip()

    if not home_team or not away_team:
        raise HTTPException(status_code=400, detail="Takım isimleri boş olamaz")

    if home_team.lower() == away_team.lower():
        raise HTTPException(status_code=400, detail="Aynı takım kendiyle eşleşemez")

    team1_data = get_team_elo(home_team)
    team2_data = get_team_elo(away_team)

    if not team1_data or not team2_data:
        raise HTTPException(status_code=404, detail="Takımlardan biri bulunamadı")

    analysis = analyze_match(team1_data, team2_data)

    return {
        "success": True,
        "match": f"{team1_data.get('team', home_team)} vs {team2_data.get('team', away_team)}",
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
