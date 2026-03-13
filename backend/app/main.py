from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Futbol Analiz API çalışıyor"}

@app.get("/health")
def health():
    return {"status": "ok"}
