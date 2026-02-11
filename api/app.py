from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()
STATUS_FILE = "status.json"

class StatusUpdate(BaseModel):
    status: str  # coding, free, meeting, on-way, ...

@app.get("/status")
def get_status():
    try:
        with open(STATUS_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"WORK_STATUS": "free"}
    return data

@app.post("/status")
def set_status(update: StatusUpdate):
    data = {"WORK_STATUS": update.status}
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f)
    return {"status": update.status}
