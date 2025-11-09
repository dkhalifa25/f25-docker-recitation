from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

MICROSERVICE_LINK = "https://appbox.qatar.cmu.edu/313-teams/team_name/"

# Correct team-to-mentor mapping
MENTORS = {
    "1": "Seckhen",  # Team 1
    "2": "Aadi",     # Team 2
    "3": "Steve",    # Team 3
    "4": "Seckhen",  # Team 4
    "5": "Aadi",     # Team 5
    "6": "Steve",    # Team 6
}

@app.get("/")
def root():
    return {"ok": True, "message": "Team Info Service is running"}

@app.get("/team_info/{team_id}")
def get_team_info(team_id: str):
    if not team_id:
        raise HTTPException(status_code=400, detail="Missing team id")

    team_id = team_id.strip().lower()

    if team_id not in MENTORS:
        raise HTTPException(status_code=404, detail="Invalid team id")

    try:
        resp = requests.get(MICROSERVICE_LINK + team_id, timeout=5)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error contacting microservice: {e}")

    try:
        data = resp.json()
        team_name = data.get("team_name")
    except Exception:
        raise HTTPException(status_code=502, detail="Invalid JSON from upstream service")

    if not team_name:
        raise HTTPException(status_code=502, detail="Upstream response missing team_name")

    return {
        "team_id": int(team_id),
        "team_name": team_name,
        "mentor": MENTORS[team_id],
    }
