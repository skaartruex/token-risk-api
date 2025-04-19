import requests
from datetime import datetime

BIRDEYE_API_KEY = "your_birdeye_api_key"
HEADERS = {"X-API-KEY": BIRDEYE_API_KEY}
BASE_URL = "https://public-api.birdeye.so/public"

def fetch_token_data(token_address):
    info = requests.get(f"{BASE_URL}/token/{token_address}", headers=HEADERS).json()["data"]
    holders = requests.get(f"{BASE_URL}/token/{token_address}/holders", headers=HEADERS).json()["data"]
    
    return {
        "price": info["price"],
        "market_cap": info["market_cap"],
        "volume_24h": info["volume_24h"],
        "token_age_days": (datetime.now() - datetime.fromtimestamp(info["created_at"])).days,
        "holders": holders["holders_count"],
        "top_10_percent": holders["top_10_percent"]
    }

def score_risk(data):
    age_score = 100 if data["token_age_days"] > 180 else 0
    holder_score = max(0, 100 - data["top_10_percent"])
    volume_score = min(100, data["volume_24h"] / 10000 * 100)
    mcap_score = min(100, data["market_cap"] / 10000 * 100)
    
    trust_score = round(0.25 * age_score + 0.25 * holder_score + 0.25 * volume_score + 0.25 * mcap_score, 2)
    
    return {
        "trust_score": trust_score,
        "breakdown": {
            "age_score": age_score,
            "holder_score": holder_score,
            "volume_score": volume_score,
            "market_cap_score": mcap_score,
        }
    }