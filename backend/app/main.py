from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Futbol Analiz API çalışıyor"}

@app.get("/health")
def health():
    return {"status": "ok"}
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
