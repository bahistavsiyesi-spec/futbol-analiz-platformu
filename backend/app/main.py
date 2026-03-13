from fastapi import FastAPI
from app.scrapers.clubelo import get_team_elo
from app.services.analyzer import analyze_match

app = FastAPI(
    title="Futbol Analiz API",
    description="Takım Elo verilerini çekip karşılaştırma ve maç analizi yapan FastAPI servisi.",
    version="1.0.0"
)


@app.get("/", tags=["Root"], summary="Ana sayfa")
def home():
    return {
        "message": "Futbol Analiz API çalışıyor",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["System"], summary="Sağlık kontrolü")
def health():
    return {"status": "ok"}


@app.get("/team-elo/{team_name}", tags=["Teams"], summary="Takım Elo verisini getir")
def team_elo(team_name: str):
    data = get_team_elo(team_name)

    if not data:
        return {"error": "Takım bulunamadı"}

    return data


@app.get("/compare-teams/{team1}/{team2}", tags=["Analysis"], summary="İki takımı Elo ile karşılaştır")
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


@app.get("/analyze-match/{team1}/{team2}", tags=["Analysis"], summary="Maç analizini oluştur")
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


@app.get("/analyze-sample-matches", tags=["Analysis"], summary="Örnek maç listesini analiz et")
def analyze_sample_matches():
    matches = [
        {"team1": "RealMadrid", "team2": "Barcelona"},
        {"team1": "Galatasaray", "team2": "Fenerbahce"},
        {"team1": "ManchesterCity", "team2": "Liverpool"}
    ]

    results = []

    for match in matches:
        team1_data = get_team_elo(match["team1"])
        team2_data = get_team_elo(match["team2"])

        if not team1_data or not team2_data:
            results.append({
                "match": f"{match['team1']} vs {match['team2']}",
                "error": "Takımlardan biri bulunamadı"
            })
            continue

        analysis = analyze_match(team1_data, team2_data)

        results.append({
            "match": f"{team1_data.get('team', match['team1'])} vs {team2_data.get('team', match['team2'])}",
            "team1": team1_data,
            "team2": team2_data,
            "analysis": analysis
        })

    return {
        "count": len(results),
        "matches": results
    }
