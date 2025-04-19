from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from utils import fetch_token_data, score_risk

app = FastAPI(title="TrueX Token Risk API")

@app.get("/risk")
def get_token_risk(token_address: str = Query(..., description="Token address to analyze")):
    data = fetch_token_data(token_address)
    score = score_risk(data)
    return {"token_data": data, "risk_score": score}

@app.get("/.well-known/openapi.yaml")
def get_openapi():
    return FileResponse("openapi.yaml", media_type="text/yaml")# dummy change
